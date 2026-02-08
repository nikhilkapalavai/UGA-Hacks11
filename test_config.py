from app import app, LOCATION, PROJECT_ID

print(f"App imported.")
print(f"LOCATION: {LOCATION}")
print(f"PROJECT_ID: {PROJECT_ID}")

# Trigger initialization
from app import get_gemini_llm
llm = get_gemini_llm()
print(f"LLM initialized: {llm}")
