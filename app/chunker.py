from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def chunk_text(pages, chunk_size=400, chunk_overlap=50, doc_name="unknown.pdf"):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "]
    )

    all_chunks = []

    for page_num, text in pages:
        page_chunks = splitter.create_documents([text])
        for chunk in page_chunks:
            chunk.metadata = {
                "page": page_num,
                "source": doc_name
            }
            all_chunks.append(chunk)

    print(f"📄All chunks: {all_chunks}")

    return all_chunks
