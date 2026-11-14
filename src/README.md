# Source Code Documentation

## Overview

This directory contains the backend implementation of the Intelligent Bug Diagnosis Platform.

## Files

### `main.py`

Implements the FastAPI backend and bug report submission endpoint.

**Implemented features:**
- Provides a health-check endpoint (`GET /`).
- Accepts bug report titles and descriptions.
- Supports optional TXT, LOG, and JSON file uploads.
- Validates input fields and file extensions.
- Enforces a maximum upload size of 1 MB.
- Stores submitted reports locally as JSON files.
- Generates a unique ID for each submitted report.

## Running the Backend

From the project root directory, run:

```bash
uvicorn src.main:app --reload
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

## Technologies

- Python
- FastAPI
- Uvicorn
- JSON

## Current Limitations

- No frontend interface is implemented yet.
- Authentication is not implemented.
- Bug diagnosis agents are not implemented yet.
- Uploaded files are stored locally.
