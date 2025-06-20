from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

index = faiss.IndexFlatL2(384)
doc_store = {}

def embed_chunks(document_id, chunks):
    vectors = model.encode([chunk.page_content for chunk in chunks])
    faiss.normalize_L2(vectors)
    index.add(np.array(vectors))
    doc_store[document_id] = chunks

    # Log the number of vectors now in the FAISS index
    print(f"✅ Added {len(vectors)} vectors for document ID: {document_id}")
    print(f"📊 Total vectors in FAISS index: {index.ntotal}")
    
    return len(vectors)
