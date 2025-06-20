# Document Intelligence RAG Chatbot

## 🧠 Description
A RAG-based intelligent chatbot that allows users to query documents (PDF, DOCX, TXT) using LLMs with contextual chunk retrieval, OCR, and citations.

## 🚀 Features
- PDF/DOCX/TXT support with OCR for scanned content
- FAISS vector search
- Chunking with LangChain
- Embedding with all-MiniLM-L6-v2
- LLM answer generation using zephyr-7b-beta
- Citations and conversation tracking

## 🛠️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Install OCR and PDF support (OS specific)
- Ubuntu:
```bash
sudo apt install tesseract-ocr poppler-utils
```
- Windows:
Install [Tesseract](https://github.com/tesseract-ocr/tesseract) and [Poppler](https://github.com/oschwartz10612/poppler-windows)

### 3. Run the API
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 📬 API Endpoints

### POST `/api/embedding`
Upload and embed a document.

### POST `/api/query`
Query the document and get LLM-generated answers with citations.

# API Test Script for Document RAG Chatbot

This script, [test_api.py](test_api.py), provides a command-line interface to interact with the Document RAG Chatbot API. It allows you to upload a document for embedding and then interactively query the chatbot using the embedded document.

## Features

- Uploads a document (PDF, DOCX, or TXT) to the `/api/embedding` endpoint.
- Receives a `document_id` for future queries.
- Allows interactive querying of the chatbot via the `/api/query` endpoint.
- Maintains conversation context using `conversation_id`.

## Usage

1. **Ensure the API server is running** 

2. **Run the test script**

   ```sh
   python test_api.py
   ```

3. **Follow the prompts:**
   - Enter the path to the document you want to upload.
   - After successful embedding, enter your queries one by one.
   - Type `exit` to quit the chat.

## Example

```
📁 Enter the path to the document: C:\Users\LENOVO\Downloads\Inputs\Inputs\NIFTY 50 Annual Report.docx
📄 Uploading document for embedding...
✅ Embedding Response: {
  "status": "success",
  "message": "Document embedded successfully.",
  "document_id": "..."
}

🔍 Enter your query (type 'exit' to quit): What is the main topic?
💬 Sending query to the RAG chatbot...
✅ Query Response: {
  "status": "success",
  "response": {
    "answer": "...",
    "citations": [...]
  },
  "conversation_id": "..."
}
```

## 📊 Evaluation Methodology

To ensure robust model selection, I defined a set of key evaluation metrics spanning the full RAG (Retrieval-Augmented Generation) pipeline. These include:

![Metric for Evaluation](./Metric.png)

- **Content Quality**:  
  - *Chunk Quality*: Chunks must accurately represent the source content.  
  - *Chunk Size*: Optimized for embedding and retrieval.  
  - *Metadata Accuracy*: Correct attribution to source document and page.

- **Retrieval Quality**:  
  - *Relevance of Retrieved Documents*: Degree to which documents align with the query.  
  - *Coverage*: Completeness of information retrieval.  
  - *Context Noise*: Avoidance of irrelevant or misleading documents.

- **Generation Quality**:  
  - *Factual Accuracy*: Response correctness.  
  - *Relevance to Query*: Response specificity.  
  - *Hallucination Rate*: Frequency of unsupported/generated content.

- **End-to-End Latency**:  
  - Total response time from query input to output.

---

## 🤖 Model Selection Justification

### ✅ Current Selection:

- **Embedding Model**: `all-MiniLM-L6-v2`  
  - Lightweight and resource-efficient  
  - Strong semantic embedding capabilities  
  - Ideal for local deployment

- **LLM**: `HuggingFaceH4/zephyr-7b-beta`  
  - Open-source and MIT licensed  
  - Efficient and chat-optimized  
  - Strong performance on assistant-style tasks
    
## ✂️ Chunking Strategy

### 🛠 Implementation

The chunking logic is implemented using LangChain's `RecursiveCharacterTextSplitter`

### ✅ Justification

- **Recursive Splitting**  
  Ensures chunks break cleanly at semantic boundaries (e.g., paragraphs, sentences), improving the quality of embeddings.

- **Chunk Size: `400`**  
  - Provides enough context for meaningful embeddings  
  - Avoids exceeding token limits of smaller models like `all-MiniLM-L6-v2`

- **Chunk Overlap: `50`**  
  Maintains context continuity across chunks, reducing information loss.

- **Metadata Attachment**  
  Each chunk includes metadata such as:
  - Page number (`"page"`)
  - Document source (`"source"`)  
  This enables traceability during document retrieval and evaluation.
