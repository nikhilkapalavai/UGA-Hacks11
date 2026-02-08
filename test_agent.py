from fastapi.testclient import TestClient
from app import app
import sys

client = TestClient(app)

def test_chat():
    print("Sending request to /chat...")
    # Ask a question that requires RAG
    query = "Recommend a CPU for a budget gaming PC"
    response = client.post("/chat", json={"message": query})
    
    if response.status_code == 200:
        print("\nSuccess! API Response:")
        print(response.json())
    else:
        print(f"\nFailed with status {response.status_code}:")
        print(response.text)

if __name__ == "__main__":
    test_chat()
