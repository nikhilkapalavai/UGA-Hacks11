import requests
import json
import time

url = "http://localhost:8000/build-pc"
payload = {
    "query": "A futuristic white gaming PC with RGB, $2500 budget",
    "verbose": True
}

print("Testing Visualization Agent...")
print(f"Sending request to {url}...")

try:
    start_time = time.time()
    response = requests.post(url, json=payload)
    end_time = time.time()
    
    if response.status_code == 200:
        data = response.json()
        viz = data.get("reasoning", {}).get("stage_4_visualization", {})
        
        print("\n--- Visualization Result ---")
        print(f"Source: {viz.get('source')}")
        print(f"Image URL: {viz.get('image_url')}")
        print(f"Prompt: {viz.get('prompt')}")
        print(f"Total Time: {end_time - start_time:.2f}s")
        
        if viz.get("image_url"):
            print("✅ SUCCESS: Image URL returned.")
        else:
            print("❌ FAILURE: No Image URL.")
            
    else:
        print(f"❌ Error {response.status_code}: {response.text}")

except Exception as e:
    print(f"❌ Exception: {e}")
