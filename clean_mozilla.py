
import json
from pathlib import Path

# Read the original dataset
input_file = Path("datasets/raw/mozilla_sample.json")

with input_file.open("r", encoding="utf-8") as file:
    data = json.load(file)

bugs = data.get("bugs", [])

# Clean and standardize the records
cleaned_bugs = []

for bug in bugs:
    cleaned_bug = {
        "id": bug.get("id"),
        "summary": (bug.get("summary") or "").strip(),
        "status": (bug.get("status") or "").strip(),
        "resolution": bug.get("resolution") or None,
        "product": (bug.get("product") or "").strip(),
        "component": (bug.get("component") or "").strip(),
        "creation_time": bug.get("creation_time")
    }

    cleaned_bugs.append(cleaned_bug)

# Create processed folder
output_folder = Path("datasets/processed")
output_folder.mkdir(parents=True, exist_ok=True)

# Save cleaned dataset
output_file = output_folder / "mozilla_cleaned.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(
        {"bugs": cleaned_bugs},
        file,
        indent=4,
        ensure_ascii=False
    )

print("Cleaning completed!")
print("Total records:", len(cleaned_bugs))
print("Saved to:", output_file)
