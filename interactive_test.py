from fastapi.testclient import TestClient
from app import app
import sys

# Initialize the test client
client = TestClient(app)

def interactive_chat():
    print("--- PC Part Picker AI Interactive Test ---")
    print("Type 'quit' or 'exit' to stop.")
    
    while True:
        try:
            print("\nYou: ", end="", flush=True)
            user_input = input()
        except EOFError:
            break
            
        if user_input.lower() in ["quit", "exit"]:
            break
            
        print("BuildBuddy is thinking...", flush=True)
        try:
            response = client.post("/chat", json={"message": user_input})
            
            if response.status_code == 200:
                data = response.json()
                print(f"BuildBuddy: {data.get('response', 'No response text')}", flush=True)
            else:
                print(f"Error {response.status_code}: {response.text}", flush=True)
                
        except EOFError:
            break
        except Exception as e:
            print(f"Error: {e}")
            break

if __name__ == "__main__":
    interactive_chat()
