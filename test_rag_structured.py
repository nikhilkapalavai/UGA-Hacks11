import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
DATA_STORE_ID = os.getenv("VERTEX_SEARCH_DATA_STORE_ID")

print(f"Testing Structured RAG with Project: {PROJECT_ID}, Data Store: {DATA_STORE_ID}")

try:
    from langchain_google_community import VertexAISearchRetriever
    
    # Try engine_data_type=1 for Structured
    retriever = VertexAISearchRetriever(
        project_id=PROJECT_ID,
        location_id="global",
        data_store_id=DATA_STORE_ID,
        max_documents=3,
        engine_data_type=1, 
        get_extractive_answers=True
    )
    
    query = "AMD"
    print(f"Running Query: '{query}' with engine_data_type=1...")
    
    results = retriever.invoke(query)
    
    if not results:
        print("Found 0 results with engine_data_type=1.")
    else:
        print(f"Success! Found {len(results)} results:")
        for i, doc in enumerate(results):
            print(f"\nResult {i+1}:")
            print(f"Content: {doc.page_content[:200]}...")
                
except Exception as e:
    print(f"Error: {e}")
