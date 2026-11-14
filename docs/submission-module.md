# Bug Report Submission Module

## 1. Overview
The submission module allows users to submit bug reports through text input or file uploads. It is developed using FastAPI.

## 2. API Endpoint

- Method: POST
- Endpoint: `/submit`
- Input: Multipart form data
- Output: JSON response

## 3. Input Fields

- **Title:** Bug report title (1–200 characters).
- **Description:** Bug description (1–20,000 characters).
- **File:** Optional TXT, LOG, or JSON attachment.

## 4. Validation and Security

- Empty titles and descriptions are rejected.
- Title and description length limits are enforced.
- Only TXT, LOG, and JSON extensions are accepted.
- Maximum uploaded file size is 1 MB.
- Uploaded files must contain valid UTF-8 text.
- Unique UUIDs are generated for submitted reports.
- Original filenames are not used as storage paths.

## 5. Storage

Submitted reports are stored locally in:

`datasets/submissions/`

Each submission is saved as an individual JSON file containing the report ID, title, description, uploaded file content, and submission timestamp.

## 6. Testing Results

| Test | Result |
|---|---|
| Text-only submission | Passed |
| TXT file upload | Passed |
| Uploaded content storage | Passed |
| Unsupported file rejection | Passed |
| File-size validation | Passed |

## 7. Technology Used

- Python
- FastAPI
- Uvicorn
- JSON
- PowerShell for testing

## 8. Current Limitation

This is an initial backend prototype. Authentication, malware scanning, and production-grade storage controls have not yet been implemented.