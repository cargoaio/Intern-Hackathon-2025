import os
from dotenv import load_dotenv
import google.generativeai as genai

def list_available_models():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    
    try:
        models = genai.list_models()
        print("Available Models:")
        for m in models:
            print(f"\nName: {m.name}")
            print(f"Display Name: {m.display_name}")
            print(f"Description: {m.description}")
            print("-" * 50)
    except Exception as e:
        print(f"Error listing models: {str(e)}")

if __name__ == "__main__":
    list_available_models()