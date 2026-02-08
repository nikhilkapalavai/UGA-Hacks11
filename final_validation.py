from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_chat():
    queries = [
        "Search for AMD processors",
        "Tell me about the RTX 5090"
    ]
    
    for query in queries:
        print(f"\nUser: {query}")
        response = client.post("/chat", json={"message": query})
        if response.status_code == 200:
            print(f"BuildBuddy: {response.json()['response']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    test_chat()
