# Dataset Documentation

## Overview

This directory contains the datasets used to build and test the historical bug knowledge base for the Intelligent Bug Diagnosis Platform.

## Dataset Source

**Mozilla Bugzilla REST API**

- Source: https://bugzilla.mozilla.org/
- Product: Firefox
- Collection method: Public REST API
- API authentication: Not required for this sample

## Directory Structure

```text
datasets/
├── raw/
│   └── mozilla_sample.json
├── processed/
│   ├── mozilla_cleaned.json
│   ├── mozilla_chunks.json
│   └── mozilla_embeddings.json
├── submissions/
├── vector_db/
├── dataset-inspection.md
└── retrieval-evaluation.md
```

## Data Processing Pipeline

1. **Collection:** Downloaded 10 Firefox bug reports from Mozilla Bugzilla.
2. **Inspection:** Checked missing values and duplicate bug IDs.
3. **Cleaning:** Standardized fields and removed unnecessary whitespace.
4. **Chunking:** Split each report into summary and resolution chunks when available.
5. **Embedding Generation:** Generated 384-dimensional vectors using `all-MiniLM-L6-v2`.
6. **Vector Storage:** Stored the chunks and embeddings in ChromaDB.
7. **Retrieval:** Tested semantic search using sample bug-related queries.

## Current Dataset Statistics

| Item | Count |
|---|---:|
| Downloaded bug reports | 10 |
| Cleaned bug reports | 10 |
| Generated text chunks | 16 |
| Generated embeddings | 16 |
| Embedding dimensions | 384 |

## Data Handling

- Raw data is preserved separately from processed data.
- Missing resolution values are retained as `null`.
- Processed files are stored in JSON format.
- The vector database is stored locally.

## Limitations

- The current implementation uses only a small Mozilla sample.
- Apache and Eclipse datasets have not yet been integrated.
- Retrieval quality needs evaluation using a larger and more diverse dataset.
- The current results demonstrate a prototype, not a production-ready knowledge base.

## Future Work

- Expand the knowledge base with Apache and Eclipse defect reports.
- Increase the dataset size.
- Improve chunking and retrieval quality.
- Evaluate retrieval using relevant metrics such as Precision@K and Recall@K.