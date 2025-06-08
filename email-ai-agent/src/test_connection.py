import os
from dotenv import load_dotenv
from openai import OpenAI

def test_connection():
    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")
    
    if not api_key:
        print("API key not found in environment variables")
        return
        
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": "Hello, can you hear me?"}
            ]
        )
        
        print("Connection successful!")
        print("Response:", response.choices[0].message.content)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_connection()