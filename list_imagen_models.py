import os
from google.cloud import aiplatform

PROJECT_ID = "uga-hacks11"
LOCATION = "us-central1"

aiplatform.init(project=PROJECT_ID, location=LOCATION)

print(f"Listing models for {PROJECT_ID} in {LOCATION}...")

try:
    print("\nChecking ImageGenerationModel availability...")
    from vertexai.preview.vision_models import ImageGenerationModel
    
    for model_name in ["imagegeneration@006", "imagegeneration@005", "imagen-3.0-generate-001"]:
        try:
            print(f"Testing access to: {model_name}")
            model = ImageGenerationModel.from_pretrained(model_name)
            # Just try to load it, generation might fail due to billing but loading should work if model exists
            print(f"✅ Loaded: {model_name}")
        except Exception as e:
            print(f"❌ Failed to load: {model_name} - {e}")

except Exception as e:
    print(f"Global Error: {e}")
