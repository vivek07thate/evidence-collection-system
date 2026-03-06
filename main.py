from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from postgresql_db import engine, SessionLocal
import models
from models import Evidence

from embeddings_model import generate_embedding, embedding_dimension
from vector_store import (
    add_document,
    similarity_search,
    delete_document,
    get_vector_dimension,
    delete_all_embeddings
)
from object_storage import minio_client, bucket_name
from rag_llm import ask_llm

from datetime import datetime
from io import BytesIO
import uuid

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return {"message": "Evidence Collection System Running 🚀"}


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("static/index.html", encoding="utf-8") as f:
        return HTMLResponse(content=f.read(), media_type="text/html; charset=utf-8")



@app.post("/upload-evidence")
def upload_evidence(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_name = file.filename

    file_bytes = file.file.read()

    if not file_bytes:
        return {"error": "File is empty ❌"}
    
    db = SessionLocal()

    # 🔥 Check duplicate before processing
    existing = db.query(Evidence).filter(
        Evidence.file_name == file.filename
    ).first()

    if existing:
        db.close()
        return {"message": "File already uploaded ❌"}

    file_id = str(uuid.uuid4())

    # Store file in MinIO
    minio_client.put_object(
        bucket_name,
        file_id,
        BytesIO(file_bytes),
        length=len(file_bytes),
        content_type=file.content_type
    )

    # Extract text
    try:
        text = file_bytes.decode("utf-8")
    except:
        text = "Unsupported file type"

    # Generate embedding
    embedding = generate_embedding(text)

    # Store in ChromaDB
    add_document(
        doc_id=file_id,
        text=text,
        embedding=embedding,
        metadata={"file_name": file_name}
    )

    # Store metadata in PostgreSQL
    db = SessionLocal()
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

    query_embedding = generate_embedding(query)
    results = similarity_search(query_embedding, top_k)

    return {
        "matched_ids": results["ids"],
        "matched_documents": results["documents"],
        "similarity_scores": results["distances"]
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

    query_embedding = generate_embedding(query)
    results = similarity_search(query_embedding, top_k=3)

    matched_docs = results["documents"][0]
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

