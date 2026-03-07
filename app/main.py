from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.db.database import engine, SessionLocal
import app.db.models as models
from app.db.models import Evidence

from app.services.embedding_service import generate_embedding, embedding_dimension
from app.services.vector_service import (
    add_document,
    similarity_search,
    delete_document,
    get_vector_dimension,
    delete_all_embeddings
)
from app.services.storage_service import minio_client, bucket_name
from app.services.llm_service import ask_llm
from app.services.file_processor import process_file

from datetime import datetime
from io import BytesIO
import uuid
import os

app = FastAPI(title="Evidence Collection System")

# Create tables if not exists
models.Base.metadata.create_all(bind=engine)

# Get absolute path for static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(BASE_DIR, "static")

# Mount static folder
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/")
def root():
    return {"message": "Evidence Collection System Running 🚀"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    index_path = os.path.join(static_dir, "index.html")
    with open(index_path, encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), media_type="text/html; charset=utf-8")


@app.post("/upload-evidence")
def upload_evidence(file: UploadFile = File(...)):

    file_name = file.filename
    file_bytes = file.file.read()

    if not file_bytes:
        return {"error": "File is empty ❌"}
    
    db = SessionLocal()

    # 🔥 Check duplicate by file name only
    existing = db.query(Evidence).filter(
        Evidence.file_name == file_name
    ).first()

    if existing:
        db.close()
        return {"message": "File already uploaded ❌"}

    # Extract text using file_processor
    result = process_file(file_bytes, file_name, file.content_type)
    text = str(result["text"]).strip()  # Ensure it's a string

    if not text or "Error extracting" in text or "Warning: No text detected" in text:
        db.close()
        return {"error": "Cannot generate embeddings for empty or invalid text."}

    try:
        # Generate embedding
        embedding = generate_embedding(text)
    except Exception as e:
        db.close()
        return {"error": f"Failed to generate embedding: {str(e)}"}

    file_id = str(uuid.uuid4())

    # Store file in MinIO
    minio_client.put_object(
        bucket_name,
        file_id,
        BytesIO(file_bytes),
        length=len(file_bytes),
        content_type=file.content_type
    )

    # Store in ChromaDB
    add_document(
        doc_id=file_id,
        text=text,
        embedding=embedding,
        metadata={"file_name": file_name}
    )

    # Store metadata in PostgreSQL
    evidence = Evidence(
        id=file_id,
        file_name=file_name,
        file_size=str(len(file_bytes)),
        object_path=file_id,
        upload_time=datetime.utcnow()
    )
    db.add(evidence)
    db.commit()
    db.close()

    return {"message": "File uploaded successfully ✅", "file_id": file_id}


# =============================
# Semantic Search
# =============================
@app.post("/semantic-search")
def semantic_search_endpoint(query: str, top_k: int = 3):
    try:
        query_embedding = generate_embedding(query)
    except Exception as e:
        return {"error": f"Failed to generate query embedding: {str(e)}"}

    results = similarity_search(query_embedding, top_k)
    return {
        "matched_ids": results.get("ids", [[]])[0],
        "matched_documents": results.get("documents", [[]])[0],
        "similarity_scores": results.get("distances", [[]])[0]
    }


# =============================
# Delete Embedding
# =============================
@app.delete("/delete-embedding/{doc_id}")
def delete_embedding(doc_id: str):
    delete_document(doc_id)
    return {"message": f"{doc_id} deleted successfully"}

@app.delete("/delete-all-embeddings")
def delete_all_embeddings_endpoint():
    delete_all_embeddings()
    return {"message": "All embeddings deleted successfully ✅"}


# =============================
# Vector Dimension
# =============================
@app.get("/vector-dimension")
def vector_dimension():
    return {"dimension": embedding_dimension()}


# =============================
# Ask LLM (RAG)
# =============================
@app.post("/ask")
def ask_question(query: str):

    try:
        query_embedding = generate_embedding(query)
    except Exception as e:
        return {"error": f"Failed to generate query embedding: {str(e)}"}

    results = similarity_search(query_embedding, top_k=3)
    matched_docs = results.get("documents", [[]])[0]
    context = "\n\n".join(matched_docs)

    prompt = f"""
You are an investigation assistant.

Use the evidence below to answer.

Evidence:
{context}

Question:
{query}

Answer clearly:
"""

    answer = ask_llm(prompt)
    return {"answer": answer}
