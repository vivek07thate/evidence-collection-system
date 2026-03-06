import chromadb

client = chromadb.PersistentClient(path="./chroma_storage")

collection = client.get_or_create_collection(
    name="evidence_collection"
)

print("Document count:", collection.count())
