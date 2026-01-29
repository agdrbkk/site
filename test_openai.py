import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")

try:
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "This is a test."}
        ],
        max_tokens=5,
    )
    print("Successfully connected to OpenAI!")
    print(response.choices[0].message.content)  # ดึงข้อความจาก Response
except Exception as e:
    print(f"ERROR: Unable to connect to OpenAI. Please check your API key and permissions.\n{e}")