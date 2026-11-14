
import json
from urllib.request import Request, urlopen
from pathlib import Path

url = (
    "https://bugzilla.mozilla.org/rest/bug"
    "?product=Firefox&limit=10"
    "&include_fields=id,summary,status,resolution,"
    "product,component,creation_time"
)

request = Request(
    url,
    headers={"User-Agent": "BugDiagnosisPlatform/1.0"}
)

with urlopen(request, timeout=30) as response:
    data = json.loads(response.read().decode("utf-8"))

output_folder = Path("datasets/raw")
output_folder.mkdir(parents=True, exist_ok=True)

output_file = output_folder / "mozilla_sample.json"

with output_file.open("w", encoding="utf-8") as file:
    json.dump(data, file, indent=4, ensure_ascii=False)

print("Download completed!")
print("Number of bug reports:", len(data.get("bugs", [])))
print("Saved to:", output_file)
