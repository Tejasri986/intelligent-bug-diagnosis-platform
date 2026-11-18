
import json
from pathlib import Path
from src.agents.triage_agent import run_triage

file_path = Path("datasets/raw/mozilla_sample.json")

with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

bugs = data["bugs"]

print(f"Historical bug reports found: {len(bugs)}\n")

for bug in bugs:
    summary = bug.get("summary", "")
    report_id = str(bug.get("id", "UNKNOWN"))

    result = run_triage(report_id, summary)

    print("Bug ID:", report_id)
    print("Original component:", bug.get("component"))
    print("Bug summary:", summary)
    print("Predicted component:", result.affected_component)
    print("Severity:", result.severity)
    print("Priority:", result.priority)
    print("-" * 40)
