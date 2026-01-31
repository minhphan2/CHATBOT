from email.mime import text
from time import time
from openai import OpenAI
import os
import dotenv
import groq
from sentence_transformers import SentenceTransformer

dotenv.load_dotenv()

class LLMClient:
    def __init__(self):
        self.client = groq.Client(api_key = os.getenv("GROQ_API_KEY"))
        if not os.getenv("GROQ_API_KEY"):
            raise RuntimeError("GROQ_API_KEY not set")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')


    
    import time

    def generate(self, messages: list[dict], retries=2, delay=5) -> str:
        for i in range(retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=messages,
                    temperature=0.2
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                if i == retries:
                    raise
            print(f"Lỗi khi gọi LLM: {e}. Thử lại sau {delay} giây...")
            time.sleep(delay)
    
    def get_embedding(self, text: str) -> list[float]:
        return self.embedder.encode(text).tolist()
    
    
