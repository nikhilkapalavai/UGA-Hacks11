import os
from dotenv import load_dotenv
from google.cloud import discoveryengine

load_dotenv()

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
DATA_STORE_ID = os.getenv("VERTEX_SEARCH_DATA_STORE_ID")

def list_documents():
    client = discoveryengine.DocumentServiceClient()
    parent = client.branch_path(
        project=PROJECT_ID,
        location=LOCATION,
        data_store=DATA_STORE_ID,
        branch="default_branch",
    )

    print(f"Checking documents in: {parent}")
    
    try:
        request = discoveryengine.ListDocumentsRequest(parent=parent)
        page_result = client.list_documents(request=request)
        
        count = 0
        for doc in page_result:
            count += 1
            if count <= 5:
                print(f"Found Doc: {doc.id}")
        
        print(f"Total documents found (first page): {count}")
        
        if count == 0:
            print("No documents found. Import might have failed or is still processing.")
        else:
            print("Documents exist! Indexing might just be lagging.")
            
    except Exception as e:
        print(f"Error listing documents: {e}")

if __name__ == "__main__":
    list_documents()
