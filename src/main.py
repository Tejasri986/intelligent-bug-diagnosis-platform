
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime, timezone
import json
import uuid

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
STORAGE_DIR = BASE_DIR / "datasets" / "submissions"

# Create storage directory if it does not exist
STORAGE_DIR.mkdir(parents=True, exist_ok=True)

# FastAPI application
app = FastAPI(
    title="Intelligent Bug Diagnosis Platform",
    description="AI-powered software bug diagnosis platform"
)

# Serve frontend CSS and JavaScript
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)

# Upload settings
MAX_FILE_SIZE = 1 * 1024 * 1024  # 1 MB
ALLOWED_EXTENSIONS = {".txt", ".log", ".json"}


# Dashboard route
@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


# Bug report submission API
@app.post("/submit")
async def submit_bug_report(
    title: str = Form(...),
    description: str = Form(...),
    file: UploadFile | None = File(None)
):
    title = title.strip()
    description = description.strip()

    # Validate title
    if not title or len(title) > 200:
        raise HTTPException(
            status_code=400,
            detail="Title must contain 1–200 characters"
        )

    # Validate description
    if not description or len(description) > 20000:
        raise HTTPException(
            status_code=400,
            detail="Description must contain 1–20000 characters"
        )

    file_content = None

    # Validate optional uploaded file
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

    # Create bug report
    report = {
        "report_id": str(uuid.uuid4()),
        "title": title,
        "description": description,
        "file_content": file_content,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }

    # Save report locally
    output_file = STORAGE_DIR / f"{report['report_id']}.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)

    return {
        "message": "Bug report submitted successfully",
        "report_id": report["report_id"]
    }
