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
📁 Enter the path to the document: "C:\Users\LENOVO\Downloads\Inputs\Inputs\NIFTY 50 Annual Report.docx"
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