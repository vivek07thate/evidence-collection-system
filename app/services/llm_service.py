import requests
from app.core.config import OLLAMA_URL, LLM_MODEL_NAME

def ask_llm(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": LLM_MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception(f"LLM Error: {response.text}")

    return response.json()["response"]
