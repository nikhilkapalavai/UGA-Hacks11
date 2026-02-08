import os
from langchain_google_vertexai import ChatVertexAI
from langchain.tools import Tool, tool
from google.cloud import discoveryengine_v1beta as discoveryengine

PROJECT_ID = "uga-hacks11"
LOCATION = "us-central1"

print(f"Testing Google Search Grounding for {PROJECT_ID}...")

def search_google(query: str):
    """Searches Google for real-time information."""
    # Note: Vertex AI Search Grounding is typically done via the model directly
    # or via a dedicated tool if your project has "Google Search" indexing enabled in Vertex Agent Builder.
    # However, for the hackathon, the easiest way to get "Grounding" is using the 
    # `tools=[GoogleSearchRetrieval]` in Gemini.
    
    from vertexai.preview.generative_models import GenerativeModel, Tool
    from vertexai.preview.generative_models import grounding
    
    model = GenerativeModel("gemini-2.0-flash-exp")
    tools = [Tool.from_google_search_retrieval(grounding.GoogleSearchRetrieval())]
    
    response = model.generate_content(
        query,
        tools=tools,
        generation_config={"temperature": 0.0}
    )
    
    return response.text

try:
    import vertexai
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    
    query = "current price of RTX 4090"
    print(f"Querying: {query}")
    result = search_google(query)
    print("\n--- Result ---")
    print(result)
    print("✅ Success: Google Search Grounding works.")

except Exception as e:
    print(f"\n❌ Error: {e}")
