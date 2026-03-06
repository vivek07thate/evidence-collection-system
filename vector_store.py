import chromadb

# Persistent storage
client = chromadb.PersistentClient(path="./chroma_storage")

collection = client.get_or_create_collection(
    name="evidence_collection",
    metadata={"hnsw:space": "cosine"}
)

def add_document(doc_id, text, embedding, metadata):
    collection.add(
        ids=[doc_id],
        documents=[text],
        embeddings=[embedding],
        metadatas=[metadata]
    )

def similarity_search(query_embedding, top_k=3):
    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

def delete_document(doc_id):
    collection.delete(ids=[doc_id])

def delete_all_embeddings():
    client.delete_collection(name="evidence_collection")
    
    global collection
    collection = client.get_or_create_collection(
        name="evidence_collection",
        metadata={"hnsw:space": "cosine"}
    )

def get_vector_dimension():
    test_vector = collection.get(limit=1, include=["embeddings"])
    if test_vector["embeddings"]:
        return len(test_vector["embeddings"][0])
    return 0