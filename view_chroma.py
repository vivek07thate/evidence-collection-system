import chromadb

client = chromadb.PersistentClient(path="./chroma_storage")

collection = client.get_collection("evidence_collection")

data = collection.get(
    include=["documents", "metadatas", "embeddings"]
)

print("Total Documents:", len(data["ids"]))
print("--------------------------------------------------")

for i in range(len(data["ids"])):
    print(f"ID: {data['ids'][i]}")
    print(f"Document: {data['documents'][i]}")
    print(f"Metadata: {data['metadatas'][i]}")
    print(f"Embedding Dimension: { data['embeddings'][i][:10]}...)")
    print("--------------------------------------------------")