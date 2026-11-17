
from fastapi import FastAPI, Form, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime, timezone
from src.agents import run_triage, analyze_logs
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

def run_bug_analysis(report_id: str, title: str, description: str, file_content: str = ""):
    combined_text = f"{title}\n{description}\n{file_content}"

    triage_result = run_triage(report_id, combined_text)
    log_result = analyze_logs(file_content)

    return {
        "report_id": report_id,
        "triage": triage_result.model_dump(),
        "log_analysis": log_result.model_dump()
    }
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
        # Create bug report
    report_id = str(uuid.uuid4())

    report = {
        "report_id": report_id,
        "title": title,
        "description": description,
        "file_content": file_content,
        "submitted_at": datetime.now(timezone.utc).isoformat()
    }

    # Run Triage and Log Analysis agents
    analysis_result = run_bug_analysis(
        report_id,
        title,
        description,
        file_content or ""
    )

    report["analysis"] = analysis_result

    # Save report locally
    output_file = STORAGE_DIR / f"{report_id}.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=4, ensure_ascii=False)
