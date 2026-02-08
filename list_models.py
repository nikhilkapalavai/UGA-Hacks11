import os
from google.cloud import aiplatform

PROJECT_ID = "uga-hacks11"
LOCATION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

print(f"Listing models for {PROJECT_ID} in {LOCATION}...")

try:
    models = aiplatform.Model.list()
    if not models:
        print("No custom models found (this is expected for Gemini as it's a publisher model).")

    print("\nChecking GenerativeModel availability...")
    from vertexai.preview.generative_models import GenerativeModel
    
    for model_name in ["gemini-1.5-pro-001", "gemini-1.5-flash-001", "gemini-1.0-pro-001"]:
        try:
            model = GenerativeModel(model_name)
            print(f"✅ Success: {model_name} is accessible.")
        except Exception as e:
            print(f"❌ Failed: {model_name} - {e}")

except Exception as e:
    print(f"Global Error: {e}")
