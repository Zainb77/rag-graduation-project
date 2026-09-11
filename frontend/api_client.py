import os
import requests
from dotenv import load_dotenv
 
load_dotenv()

 
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def query_backend(question: str):
    """إرسال السؤال إلى FastAPI Backend واسترجاع الإجابة مع المصادر."""
    try:
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"question": question},
            timeout=30
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "answer": f"⚠️ Server Error ({response.status_code}): Unable to fetch response.",
                "sources": []
            }
    except requests.exceptions.RequestException as e:
        return {
            "answer": f"🔌 Connection Error: Failed to connect to backend at {API_BASE_URL}.",
            "sources": []
        }