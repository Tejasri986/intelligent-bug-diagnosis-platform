# Semantic Similarity and Embeddings

## 1. Semantic Similarity

Semantic similarity is the process of measuring how closely two pieces of text are related in meaning.

Example:

- Bug 1: Application crashes during login.
- Bug 2: App stops working when the user signs in.

Although the words are different, both reports describe a similar problem.

## 2. Text Embeddings

An embedding is a numerical representation of text. An embedding model converts sentences or documents into numerical vectors that capture semantic information.

Example:

Input: "Application crashes during login."

Output: A numerical vector such as [0.21, 0.45, 0.78, 0.12, ...]

## 3. Cosine Similarity

Cosine similarity is a mathematical technique used to measure the similarity between two vectors.

- Value close to 1: Vectors are highly aligned.
- Value close to 0: Vectors are less aligned.
- Value close to -1: Vectors point in opposite directions.

## 4. Role in Our Project

Our Intelligent Bug Diagnosis Platform will use semantic similarity to find historical bug reports related to a newly submitted issue.

Proposed technologies:

- Sentence Transformers: Generates text embeddings.
- ChromaDB: Stores and searches vector embeddings.
- Cosine Similarity: Measures vector similarity.

## 5. Advantages

- Finds bugs with similar meanings.
- Works even when different words are used.
- Helps detect duplicate or related bug reports.
- Improves historical defect retrieval.

## 6. Conclusion

Semantic similarity and embeddings help computers understand relationships between text. They are important for finding related historical bugs and supporting automated bug diagnosis.
