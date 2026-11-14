import chromadb
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to local database
client = chromadb.PersistentClient(
    path="datasets/vector_db"
)

collection = client.get_collection(
    name="mozilla_bug_reports"
)

# Sample bug query
query = "Firefox default open and save directory is not smart"

# Convert query into embedding
query_embedding = model.encode(query).tolist()

# Search similar bug reports
results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

print("\nSimilar Bug Reports")
print("-------------------")

for document, metadata, distance in zip(
    results["documents"][0],
    results["metadatas"][0],
    results["distances"][0]
):
    print("\nBug ID:", metadata["bug_id"])
    print("Type:", metadata["chunk_type"])
    print("Description:", document)
    print("Distance:", distance)