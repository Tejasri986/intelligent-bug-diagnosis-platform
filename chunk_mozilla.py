
import json
from pathlib import Path

input_file = Path("datasets/processed/mozilla_cleaned.json")

with input_file.open("r", encoding="utf-8") as file:
    data = json.load(file)

bugs = data["bugs"]
chunks = []

for bug in bugs:

    # Create a summary chunk
    summary_text = (
        f"Bug Summary: {bug['summary']}\n"
        f"Product: {bug['product']}\n"
        f"Component: {bug['component']}"
    )

    chunks.append({
        "chunk_id": f"{bug['id']}_summary",
        "bug_id": bug["id"],
        "source": "Mozilla",
        "chunk_type": "summary",
        "text": summary_text
    })

    # Create a resolution chunk only if available
    if bug["resolution"]:
        resolution_text = (
            f"Bug Summary: {bug['summary']}\n"
            f"Resolution: {bug['resolution']}"
        )

        chunks.append({
            "chunk_id": f"{bug['id']}_resolution",
            "bug_id": bug["id"],
            "source": "Mozilla",
            "chunk_type": "resolution",
            "text": resolution_text
        })

output_folder = Path("datasets/processed")
output_file = output_folder / "mozilla_chunks.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(chunks, file, indent=4, ensure_ascii=False)

print("Chunking completed!")
print("Original bug reports:", len(bugs))
print("Generated chunks:", len(chunks))
print("Saved to:", output_file)
