import os

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:Iamvivek@localhost:5432/evidence_db")

# MinIO
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET_NAME = "evidence"

# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
LLM_MODEL_NAME = "qwen2.5:1.5b"

# Vector Store
CHROMA_PERSIST_DIRECTORY = "./chroma_storage"
VECTOR_COLLECTION_NAME = "evidence_collection"

# Tesseract
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
