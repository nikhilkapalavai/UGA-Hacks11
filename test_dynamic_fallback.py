import requests
import json
import time

url = "http://localhost:8000/build-pc"
queries = [
    "Build me a pink gaming PC",
    "I want an all-white streaming setup",
    "A powerful black RGB workstation"
]

print("Testing Dynamic Visualization Fallback...")

for query in queries:
    payload = {
        "query": query,
        "verbose": False
    }
    
    print(f"\nQuery: '{query}'")
    try:
        response = requests.post(url, json=payload)
        
        if response.status_code == 200:
            data = response.json()
            viz = data.get("reasoning", {}).get("stage_4_visualization", {})
            
            print(f"Source: {viz.get('source')}")
            print(f"Image URL: {viz.get('image_url')}")
            
            # Simple validation
            if "pink" in query.lower() and "f31405" not in viz.get('image_url', ''):
                print("⚠️ Warning: Pink URL not detected (might be using default or Vertex AI)")
            elif "white" in query.lower() and "unsplash" not in viz.get('image_url', ''):
                 print("⚠️ Warning: White URL pattern not detected")
            else:
                print("✅ match")
                
        else:
            print(f"❌ Error {response.status_code}")

    except Exception as e:
        print(f"❌ Exception: {e}")
