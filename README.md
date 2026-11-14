
# Intelligent Bug Diagnosis Platform

## Project Overview

The **Intelligent Bug Diagnosis Platform with Fix Recommendation Assistance** is a project designed to help developers understand software defects by analyzing bug reports, error messages, and stack traces.

The proposed system uses semantic similarity and Retrieval-Augmented Generation (RAG) to retrieve related historical bug reports and support future root-cause analysis and fix recommendations.

## Objectives

- Accept bug reports and error logs from users.
- Validate and store submitted bug reports.
- Build a knowledge base from historical software defects.
- Generate embeddings for semantic search.
- Retrieve similar bug reports.
- Support automated bug analysis and fix recommendations through specialized agents.

## Technology Stack

| Component | Technology |
|---|---|
| Backend API | Python, FastAPI |
| API Testing | Swagger UI |
| Text Embeddings | Sentence Transformers |
| Embedding Model | all-MiniLM-L6-v2 |
| Vector Database | ChromaDB |
| Data Processing | Python, JSON |
| Dataset Source | Mozilla Bugzilla REST API |

## Implemented Modules

### 1. Bug Report Submission Module
- Accepts bug titles and descriptions.
- Supports optional TXT, LOG, and JSON file uploads.
- Validates file extensions and file sizes.
- Limits uploaded files to 1 MB.
- Stores submitted reports locally in JSON format.

### 2. Historical Bug Knowledge Base
- Downloads sample bug reports from Mozilla Bugzilla.
- Inspects and cleans the collected data.
- Standardizes bug report fields.
- Splits reports into smaller text chunks.
- Generates 384-dimensional embeddings.
- Stores embeddings in a persistent ChromaDB collection.

### 3. Semantic Retrieval
- Converts user queries into embeddings.
- Searches the vector database for similar bug reports.
- Retrieves the top three matching results.

## Current Prototype Results

- 10 Mozilla bug reports collected.
- 10 cleaned bug records.
- 16 text chunks generated.
- 16 embeddings generated.
- Embeddings stored in ChromaDB.
- Semantic retrieval tested with sample queries.

The current dataset is a small prototype and requires expansion and further evaluation.

## Project Structure

```text
intelligent-bug-diagnosis-platform/
│
├── docs/
│   ├── project-overview.md
│   ├── literature-review.md
│   ├── system-architecture.md
│   ├── agent-design.md
│   ├── knowledge-base-design.md
│   └── submission-module.md
│
├── research/
│   ├── bug-report-structure.md
│   ├── defect-analysis.md
│   ├── rag-architecture.md
│   └── semantic-similarity.md
│
├── datasets/
│   ├── raw/
│   ├── processed/
│   ├── submissions/
│   ├── dataset-inspection.md
│   └── retrieval-evaluation.md
│
├── src/
│   └── main.py
│
├── tests/
│
├── download_mozilla.py
├── inspect_mozilla.py
├── clean_mozilla.py
├── verify_mozilla.py
├── chunk_mozilla.py
├── verify_chunks.py
├── generate_embeddings.py
├── store_embeddings.py
├── test_retrieval.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## Running the Backend

Install dependencies:

```bash
