# Retrieval Evaluation

## Objective
To evaluate whether the semantic retrieval system can identify relevant historical bug reports using natural-language queries.

## Test Results

| Test | Query | Expected Bug ID | Top Retrieved Bug ID | Result |
|---|---|---:|---:|---|
| 1 | Firefox browser crashes unexpectedly | Not established | 21482 | Poor match |
| 2 | Firefox Save As dialog folder based on URL | 21482 | 21482 | Relevant match |
| 3 | Firefox default open and save directory is not smart | 27493 | 27493 | Relevant match |

## Observations
- The system successfully generated embeddings using all-MiniLM-L6-v2.
- ChromaDB stored and retrieved the embeddings.
- Relevant historical bug reports were ranked first for two specific queries.
- The browser-crash query returned unrelated results.

## Limitations
- The current prototype uses only 10 Mozilla bug reports.
- The small dataset limits retrieval coverage and evaluation reliability.
- More historical bug reports and test queries are required for a stronger evaluation.

## Conclusion
The prototype demonstrates the basic semantic retrieval pipeline. Further testing with a larger dataset is required to improve and evaluate retrieval quality.
