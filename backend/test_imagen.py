import os
from google.cloud import aiplatform
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "uga-hacks11"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

print(f"Checking Imagen availability for {PROJECT_ID} in {LOCATION}...")

model_names = ["imagegeneration@006", "imagen-3.0-generate-001", "imagegeneration@005"]

for name in model_names:
    try:
        print(f"Testing model: {name}")
        model = ImageGenerationModel.from_pretrained(name)
        response = model.generate_images(
            prompt="A neon glowing gaming PC",
            number_of_images=1,
        )
        print(f"✅ Success: {name} works!")
        break
    except Exception as e:
        print(f"❌ Failed: {name} - {e}")
