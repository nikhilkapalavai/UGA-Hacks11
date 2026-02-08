import vertexai
from vertexai.preview.generative_models import GenerativeModel, Tool, grounding

PROJECT_ID = "uga-hacks11"
LOCATION = "us-central1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

def test_grounding():
    print("Initializing model...")
    model = GenerativeModel("gemini-2.0-flash-exp")
    
    print("Creating Google Search tool...")
    google_search_tool = Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())
    
    print("Generating content...")
    response = model.generate_content(
        "Why is the sky blue?",
        tools=[google_search_tool],
    )
    
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    try:
        test_grounding()
        print("✅ Success!")
    except Exception as e:
        print(f"❌ Error: {e}")
