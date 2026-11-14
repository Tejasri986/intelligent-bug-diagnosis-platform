
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

app = FastAPI(title="Intelligent Bug Diagnosis Platform")

# Submission storage directory
STORAGE_DIR = Path("datasets/submissions")
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB
ALLOWED_EXTENSIONS = {".txt", ".log", ".json"}


@app.get("/")
def home():
    return {"message": "Bug Diagnosis API is running"}


@app.post("/submit")
async def submit_bug_report(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile | None = File(None)
):
    title = title.strip()
    description = description.strip()

    if not title or len(title) > 200:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1–200 characters"
        )

    if not description or len(description) > 20000:
        raise HTTPException(
            status_code=400,
            detail="Description must contain 1–20000 characters"
        )

    file_content = None

    if file is not None:
        extension = Path(file.filename or "").suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Only TXT, LOG and JSON files are allowed"
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File size must not exceed 1 MB"
            )

        try:
            file_content = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(
                status_code=400,
                detail="File must contain valid UTF-8 text"
            )

    report = {
        "report_id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "file_content": file_content,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }

    output_file = STORAGE_DIR / f"{report['report_id']}.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    return {
        "message": "Bug report submitted successfully",
        "report_id": report["report_id"]
    }
