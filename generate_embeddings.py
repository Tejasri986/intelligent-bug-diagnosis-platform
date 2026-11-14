import json
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Load chunks
input_file = Path("datasets/processed/mozilla_chunks.json")

with input_file.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

# Load the embedding model
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
texts = [chunk["text"] for chunk in chunks]

print("Generating embeddings...")
embeddings = model.encode(texts)

# Attach embeddings to chunks
for chunk, embedding in zip(chunks, embeddings):
    chunk["embedding"] = embedding.tolist()

# Save results
output_file = Path("datasets/processed/mozilla_embeddings.json")

with output_file.open("w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4)

print("\nEmbedding generation completed!")
print("Total embeddings:", len(embeddings))
print("Embedding dimensions:", len(embeddings[0]))
print("Saved to:", output_file)