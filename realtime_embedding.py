from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import numpy as np

# Load model
print("Loading model...")
model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model Loaded Successfully ✅")
print("Embedding Dimension:", model.get_sentence_embedding_dimension())
print("-" * 60)

while True:
    text = input("\nEnter text (type 'exit' to quit): ")

    if text.lower() == "exit":
        print("Exiting...")
        break

    embedding = model.encode(text)

    print("\nText:", text)
    print("Embedding Dimension:", len(embedding))
    print("First 10 values:", embedding[:10])
    print("Vector Norm:", np.linalg.norm(embedding))
    print("-" * 60)