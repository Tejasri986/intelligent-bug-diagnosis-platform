
import json
from pathlib import Path

file_path = Path("datasets/processed/mozilla_cleaned.json")

with file_path.open("r", encoding="utf-8") as file:
    data = json.load(file)

bugs = data.get("bugs", [])

print("Cleaned dataset verification")
print("-----------------------------")
print("Total records:", len(bugs))

print("Unique bug IDs:", len({
    bug["id"] for bug in bugs
}))

print("Missing summaries:", sum(
    1 for bug in bugs if not bug["summary"]
))

print("Missing resolutions:", sum(
    1 for bug in bugs if bug["resolution"] is None
))

print("Verification completed!")
