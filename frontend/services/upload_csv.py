import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_URL = os.getenv("API_URL")

def upload_csv(file, session_id):
    if file is None:
        return "Please upload a file first."
    
    with open(file.name, "rb") as f:
        files = {"file": f}
        data = {"session_id": session_id}
        response = requests.post(f"{API_URL}/load_csv", files=files, data=data)
    return response.json()
