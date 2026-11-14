# RAG Architecture (Retrieval-Augmented Generation)

## 1. Introduction
RAG stands for Retrieval-Augmented Generation. It is an AI technique that combines information retrieval with text generation. It helps an AI model generate answers using relevant information from an external knowledge base.

## 2. Main Components

1. **User Query:** The developer submits a bug report or error log.
2. **Embedding Model:** Converts the submitted text into numerical vectors.
3. **Vector Database:** Stores embeddings of historical bug reports.
4. **Retriever:** Searches the vector database and retrieves similar bug reports.
5. **LLM (Large Language Model):** Uses the retrieved information and new bug report to generate a diagnosis.
6. **Output:** Provides possible root causes and fix recommendations.

## 3. Working Process

1. Collect historical bug reports.
2. Clean and divide the reports into smaller chunks.
3. Generate embeddings for each chunk.
4. Store embeddings and metadata in a vector database.
5. Receive a new bug report from the developer.
6. Generate an embedding for the new report.
7. Retrieve similar historical bugs using vector similarity search.
8. Provide the retrieved information to the LLM.
9. Generate a diagnosis and possible fix recommendations.

## 4. Application in Our Project

The Intelligent Bug Diagnosis Platform uses RAG to compare newly submitted bugs with historical defects from Mozilla, Apache, and Eclipse projects.

Proposed technologies:
- Sentence Transformers – Embedding generation.
- ChromaDB – Vector database.
- Ollama – Local LLM execution.
- Python – Backend processing.

## 5. Advantages

- Uses historical information to support diagnosis.
- Helps identify similar software defects.
- Provides relevant context to the AI model.
- Can reduce unsupported AI responses.
- Supports more informed fix recommendations.

## 6. Conclusion

RAG combines retrieval and generation to produce context-aware responses. In our platform, it helps the AI agents use historical bug reports to support software defect diagnosis.

## 7. Retrieval Evaluation

Retrieval evaluation measures how effectively the system finds relevant historical bug reports.

### Evaluation Metrics

1. **Precision@K:** Measures the proportion of retrieved results that are relevant.
2. **Recall@K:** Measures the proportion of all relevant results that are successfully retrieved.
3. **Retrieval Latency:** Measures the time taken to retrieve relevant bug reports.

### Example

If the system retrieves 10 bug reports and 8 are relevant:

Precision@10 = 8 / 10 = 80%

### Importance in Our Project

These metrics help evaluate the performance of the RAG retrieval pipeline and Duplicate Detection Agent.

They help us understand whether the system retrieves relevant historical bugs accurately and efficiently.
