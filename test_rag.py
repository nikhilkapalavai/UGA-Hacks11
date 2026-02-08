import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
DATA_STORE_ID = os.getenv("VERTEX_SEARCH_DATA_STORE_ID")

print(f"Testing RAG with Project: {PROJECT_ID}, Data Store: {DATA_STORE_ID}")
import sys
sys.stdout.flush()

try:
    from langchain_google_community import VertexAISearchRetriever
    
    retriever = VertexAISearchRetriever(
        project_id=PROJECT_ID,
        location_id="global",
        data_store_id=DATA_STORE_ID,
        max_documents=3,
        engine_data_type=1, 
        get_extractive_answers=True
    )
    
    query = "AMD"
    print(f"Running Query: '{query}'...")
    
    try:
        results = retriever.invoke(query)
        
        if not results:
            print("Success! Found 0 results (Indexing might still be in progress).")
        else:
            print(f"Success! Found {len(results)} results:")
            for i, doc in enumerate(results):
                print(f"\nResult {i+1}:")
                # Handle both object and dict access
                content = getattr(doc, 'page_content', None) or doc.get('page_content')
                print(f"Content: {content[:200]}...")
                
    except Exception as e:
        print(f"Error during retrieval: {e}")
    if "403" in str(e):
        print("\nTip: Make sure you have 'Discovery Engine API' and 'Vertex AI API' enabled in Google Cloud Console.")

except Exception as e:
    print(f"\nError: {e}")
    if "403" in str(e):
        print("\nTip: Make sure you have 'Discovery Engine API' and 'Vertex AI API' enabled in Google Cloud Console.")
