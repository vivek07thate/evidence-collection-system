import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:1.5b"   # <-- IMPORTANT

def ask_llm(prompt: str):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code != 200:
        raise Exception(f"LLM Error: {response.text}")

    return response.json()["response"]