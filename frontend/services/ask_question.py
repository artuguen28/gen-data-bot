import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

def ask_question(question, session_id):
    payload = {"question": question, "session_id": session_id}
    response = requests.post(f"{API_URL}/ask_question", json=payload)
    return response.json().get("answer", response.json())