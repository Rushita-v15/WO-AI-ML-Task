import requests
import json

# === CONFIG ===
BASE_URL = "http://localhost:8000"

# === TEST /api/embedding ===
def test_embedding(document_path):
    print("📄 Uploading document for embedding...")

    files = {
        'file': open(document_path, 'rb')
    }

    response = requests.post(f"{BASE_URL}/api/embedding", files=files)
    if response.status_code == 200:
        data = response.json()
        print("✅ Embedding Response:", json.dumps(data, indent=2))
        return data.get("document_id")
    else:
        print("❌ Failed to embed:", response.text)
        return None


def test_query(q, document_id, conversation_id=None):
    print("💬 Sending query to the RAG chatbot...")
    print("Conversation id is:", conversation_id)
    
    payload = {
        "query": q,
        "document_id": document_id,
        "require_citations": True
    }

    if conversation_id:
        payload["conversation_id"] = conversation_id

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post(f"{BASE_URL}/api/query", data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("✅ Query Response:", json.dumps(data, indent=2))
        return data.get("conversation_id")
    else:
        print("❌ Failed to query:", response)
        return conversation_id  # fallback to last known


# === MAIN TEST FLOW ===
if __name__ == "__main__":
    # Step 1: Ask user to input document path
    document_path = input("📁 Enter the path to the document: ").strip()

    # Step 2: Upload and embed document
    doc_id = test_embedding(document_path)
    if doc_id:
        conversation_id = None

        # Step 3: Loop to take user queries
        while True:
            q = input("\n🔍 Enter your query (type 'exit' to quit): ").strip()
            if q.lower() == "exit":
                print("👋 Exiting chat.")
                break

            conversation_id = test_query(q, doc_id, conversation_id)
