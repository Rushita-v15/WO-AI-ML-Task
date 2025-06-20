from app.embedding import model, index, doc_store
import numpy as np
import uuid
from huggingface_hub import InferenceClient

from constants import HUGGINGFACE_TOKEN

client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta", token=HUGGINGFACE_TOKEN)

# Conversation memory (in-memory)
conversation_history = {}

def search_similar_chunks(query, document_id, k=5):
    vector = model.encode([query])
    np_vector = np.array(vector).astype("float32")
    D, I = index.search(np_vector, k)
    matched_chunks = []
    for i in I[0]:
        if i < len(doc_store[document_id]):
            matched_chunks.append(doc_store[document_id][i])
    return matched_chunks

def extract_citations(chunks):
    citations = []
    for chunk in chunks:
        if hasattr(chunk, 'metadata'):
            citations.append({
                "page": chunk.metadata.get("page", "N/A"),
                "document_name": chunk.metadata.get("source", "N/A")
            })
    return citations

def generate_prompt(query, chunks):
    context = "\n".join([chunk.page_content for chunk in chunks])
    prompt = f"""<s>[INST] You are a helpful assistant. Use the context below to answer the user's question. Cite document name and page number.

Context:
{context}

Question: {query}
Answer: [/INST]"""
    return prompt

def generate_answer(query, document_id, conversation_id=None):
    top_chunks = search_similar_chunks(query, document_id)
    print(f"Top chunks found: {top_chunks}")

    if conversation_id:
        history = conversation_history.get(conversation_id, [])
        history.append({"query": query})
        conversation_history[conversation_id] = history
    else:
        conversation_id = str(uuid.uuid4())
        conversation_history[conversation_id] = [{"query": query}]

    prompt = generate_prompt(query, top_chunks)

    try:
        # Call Mistral LLM from Hugging Face
        response = client.text_generation(
            prompt,
            max_new_tokens=300,
            temperature=0.2,
            do_sample=True
        )
        
        answer = response.strip()
    except Exception as e:
        answer = f"[ERROR] Hugging Face call failed: {str(e)}"

    return {
        "answer": answer,
        "citations": extract_citations(top_chunks),
        "conversation_id": conversation_id
    }
