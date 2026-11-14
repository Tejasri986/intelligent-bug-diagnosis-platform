import json
from pathlib import Path
import chromadb

# Load generated embeddings
input_file = Path("datasets/processed/mozilla_embeddings.json")

with input_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

# Create a local persistent ChromaDB database
client = chromadb.PersistentClient(
    path="datasets/vector_db"
)

# Create or access collection
collection = client.get_or_create_collection(
    name="mozilla_bug_reports"
)

# Store chunks and embeddings
for chunk in chunks:
    collection.upsert(
        ids=[chunk["chunk_id"]],
        documents=[chunk["text"]],
        embeddings=[chunk["embedding"]],
        metadatas=[{
            "bug_id": str(chunk["bug_id"]),
            "source": chunk["source"],
            "chunk_type": chunk["chunk_type"]
        }]
    )

print("Storage completed!")
print("Total records:", collection.count())