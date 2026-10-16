import os
import sys
from google import genai

key = os.environ.get("GEMINI_API_KEY")
print(f"Key present: {bool(key)}")
if not key:
    print("No GEMINI_API_KEY found")
    sys.exit(0)

client = genai.Client(api_key=key)

for model_name in ["gemma-4-26b-a4b-it", "gemma-4-31b-it"]:
    print(f"\n--- Testing model: {model_name} ---")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Explain what CampusPulse AI is in one concise sentence.",
        )
        print(f"SUCCESS with {model_name}:")
        print(response.text)
    except Exception as e:
        print(f"FAILED with {model_name}: {type(e).__name__}: {e}")
