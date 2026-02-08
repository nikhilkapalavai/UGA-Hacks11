from fastapi.testclient import TestClient
from app import app
import json

client = TestClient(app)

def test_reasoning_pipeline():
    print("--- Testing Reasoning Agent (Builder -> Critic -> Refiner) ---")
    
    query = "Build me a gaming PC for $1500 playing Fortnite at 1440p."
    print(f"\nUser Query: {query}")
    
    try:
        # Call the reasoning endpoint
        response = client.post("/build-pc", json={"query": query, "verbose": True})
        
        if response.status_code == 200:
            data = response.json()
            status = data.get("status")
            final_build = data.get("build")
            reasoning = data.get("reasoning")
            
            print(f"\n[Status]: {status}")
            print("\n=== FINAL BUILD ===")
            print(json.dumps(final_build, indent=2))
            
            print("\n=== REASONING TRACE ===")
            print("Stage 1 (Draft):", "Success" if reasoning.get("stage_1_build") else "Failed")
            print("Stage 2 (Critique):", "Success" if reasoning.get("stage_2_critique") else "Failed")
            print("Stage 3 (Improvements):", "Success" if reasoning.get("stage_3_improvements") else "Failed")
                
        else:
            print(f"Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_reasoning_pipeline()
