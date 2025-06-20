import os
from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.document_loader import load_document
from app.chunker import chunk_text
from app.embedding import embed_chunks
from app.query import generate_answer

app = FastAPI()

class EmbedResponse(BaseModel):
    status: str
    message: str
    document_id: str | None = None
    error_details: str | None = None

@app.post("/api/embedding", response_model=EmbedResponse)
async def embed(file: UploadFile = File(...)):
    os.makedirs("data", exist_ok=True)
    contents = await file.read()
    path = f"data/{file.filename}"
    with open(path, "wb") as f:
        f.write(contents)

    try:
        text = load_document(path)
    except ValueError as e:
        return JSONResponse(
            status_code=400,
            content=EmbedResponse(
                status="error",
                message="Failed to process document.",
                error_details=str(e)
            ).dict()
        )

    if not any(t.strip() for _, t in text):
        return JSONResponse(
            status_code=400,
            content=EmbedResponse(
                status="error",
                message="Failed to embed document.",
                error_details="Document content is empty."
            ).dict()
        )
    
    # ✅ Generate a unique document_id
    document_id = str(uuid4())

    chunks = chunk_text(text, doc_name=file.filename)
    embed_chunks(document_id, chunks)

    return EmbedResponse(
        status="success",
        message="Document embedded successfully.",
        document_id=document_id
    )

@app.post("/api/query")
async def query_api(request: Request):
    payload = await request.json()
    query = payload.get("query")
    document_id = payload.get("document_id")
    conversation_id = payload.get("conversation_id")

    if not query or not document_id:
        return {
            "status": "error",
            "message": "Missing 'query' or 'document_id'."
        }

    try:
        result = generate_answer(query, document_id, conversation_id)
        return {
            "status": "success",
            "response": {
                "answer": result["answer"],
                "citations": result["citations"]
            },
            "conversation_id": result["conversation_id"]
        }
    except Exception as e:
        return {
            "status": "error",
            "message": "Query failed.",
            "error_details": str(e)
        }
