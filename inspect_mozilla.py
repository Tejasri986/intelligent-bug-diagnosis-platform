
import json
from pathlib import Path

file_path = Path("datasets/raw/mozilla_sample.json")

with file_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

bugs = data.get("bugs", [])

print("Total bug reports:", len(bugs))

fields = [
    "id", "summary", "status",
    "resolution", "product", "component"
]

print("\nMissing Values:")

for field in fields:
    missing = sum(
        1 for bug in bugs
        if bug.get(field) is None or bug.get(field) == ""
    )
    print(f"{field}: {missing}")

bug_ids = [bug.get("id") for bug in bugs]

print("\nDuplicate bug IDs:", len(bug_ids) - len(set(bug_ids)))

print("\nInspection completed!")
