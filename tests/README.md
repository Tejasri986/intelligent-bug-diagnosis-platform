# Testing Documentation

## Overview

This directory is reserved for automated tests of the Intelligent Bug Diagnosis Platform.

## Current Testing

The prototype has been tested manually using FastAPI Swagger UI.

| Test | Expected Result | Actual Result |
|---|---|---|
| Submit a text-only bug report | HTTP 200 | Passed |
| Upload a TXT file | HTTP 200 | Passed |
| Upload a PDF file | HTTP 400 | Passed |
| Upload a file larger than 1 MB | HTTP 413 | Passed |
| Retrieve similar bug reports | Return top 3 results | Tested |

## Test Coverage

- Bug report submission
- Input validation
- File extension validation
- File size validation
- Local JSON storage
- Semantic retrieval using ChromaDB

## Future Work

- Add automated unit tests using pytest.
- Test invalid and missing input fields.
- Test JSON file content validation.
- Test retrieval quality with a larger dataset.
- Add integration tests for the complete diagnosis workflow.

## Note

The tests performed so far are manual prototype tests. Automated test cases have not yet been implemented.