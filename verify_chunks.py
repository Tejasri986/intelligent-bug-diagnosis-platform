
import json
from pathlib import Path

file_path = Path("datasets/processed/mozilla_chunks.json")

with file_path.open("r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Chunk Verification")
print("------------------")
print("Total chunks:", len(chunks))

print("Summary chunks:", sum(
    1 for chunk in chunks
    if chunk["chunk_type"] == "summary"
))

print("Resolution chunks:", sum(
    1 for chunk in chunks
    if chunk["chunk_type"] == "resolution"
))

print("Unique bug IDs:", len({
    chunk["bug_id"] for chunk in chunks
}))

print("\nVerification completed!")
