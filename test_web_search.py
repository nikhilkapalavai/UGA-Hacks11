print("Starting test_web_search.py...")
import os
print("Imported os")
from dotenv import load_dotenv
print("Imported dotenv")
load_dotenv()
print("Loaded .env")

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
print(f"Project ID: {PROJECT_ID}")

try:
    print("Attempting to import ChatVertexAI...")
    from langchain_google_vertexai import ChatVertexAI
    print("Successfully imported ChatVertexAI")
    
    print("Attempting to import GoogleSearchRetrieval...")
    from langchain_google_vertexai import GoogleSearchRetrieval
    print("Successfully imported GoogleSearchRetrieval")
    
    if PROJECT_ID:
        print("Initializing GoogleSearchRetrieval tool...")
        # Try to initialize the tool
        search = GoogleSearchRetrieval(project_id=PROJECT_ID, location_id=LOCATION)
        print("GoogleSearchRetrieval initialized successfully.")
    else:
        print("Project ID not set, skipping initialization.")

except ImportError as e:
    print(f"ImportError: {e}")
    print("Checking alternatives...")
    try:
        from langchain_community.tools import GoogleSearchRun
        print("Found GoogleSearchRun (requires API key)")
    except ImportError:
        print("No standard Google Search tool found.")
except Exception as e:
    print(f"Error during execution: {e}")
