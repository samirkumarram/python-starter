# Day 6 – LLM Engineering Lab

## Project Overview

This project explores the basic building blocks of an LLM-powered application. It covers token counting, document chunking, embeddings, vector storage, information retrieval and answer generation using a local LLM.

The main goal was to build a simple Retrieval-Augmented Generation (RAG) system using synthetic company policy documents.

## Technologies Used

- **Python** – Main programming language
- **uv** – Python project and dependency management
- **Ollama** – Running AI models locally
- **nomic-embed-text** – Generating text embeddings
- **qwen3.5:2b** – Generating answers
- **tiktoken** – Counting tokens
- **JSON** – Storing chunks, embeddings and evaluation results

## Project Structure

```text
day-6-llm-lab/
│
├── token_lab/
│   └── token_counter.py
│
├── rag_lab/
│   ├── documents/
│   │
│   ├── chunks/
│   │   ├── fixed_size.json
│   │   ├── sentence_based.json
│   │   └── paragraph_based.json
│   │
│   ├── embeddings/
│   │
│   ├── vector_db/
│   │   ├── fixed_size.json
│   │   ├── sentence_based.json
│   │   └── paragraph_based.json
│   │
│   ├── results/
│   │   └── evaluation.json
│   │
│   ├── generate_documents.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── vector_store.py
│   └── retrieval.py
│
├── pyproject.toml
├── uv.lock
└── README.md
```

## 1. Token Counting

Created a Python script to count tokens for six different text samples:

- English prose
- Python code
- JSON data
- English text
- Hindi text
- Bengali text

Used the `tiktoken` library with the `cl100k_base` tokenizer.

Run:

```bash
uv run python token_lab/token_counter.py
```

## 2. Synthetic Policy Documents

Generated 20 synthetic company policy documents. These documents cover topics such as leave, work from home, password security, attendance, remote access, incident reporting, data retention and employee exit procedures.

The documents are stored in the `rag_lab/documents/` directory.

Run:

```bash
uv run python rag_lab/generate_documents.py
```

## 3. Document Chunking

Divided the policy documents into smaller chunks using three different strategies:

1. **Fixed-size chunking:** Divides text into groups of a fixed number of words.
2. **Sentence-based chunking:** Divides text into groups of sentences.
3. **Paragraph-based chunking:** Splits documents using paragraph boundaries.

The generated chunks are saved as JSON files inside `rag_lab/chunks/`.

Run:

```bash
uv run python rag_lab/chunking.py
```

## 4. Generating Embeddings

Used Ollama with the `nomic-embed-text` model to convert text chunks into numerical vectors.

These embeddings help the application find documents that are semantically related to a user's question.

The embeddings are saved in the `rag_lab/embeddings/` directory.

Required Ollama model:

```bash
ollama pull nomic-embed-text
```

Run:

```bash
uv run python rag_lab/embeddings.py
```

## 5. Vector Storage

Created a simple JSON-based vector store to save document information and embeddings.

Each stored record contains:

- Document name
- Chunk ID
- Original chunk text
- Embedding vector

Separate vector database files are maintained for all three chunking strategies.

This approach was used instead of a dedicated vector database.

Run:

```bash
uv run python rag_lab/vector_store.py
```

## 6. Retrieval and Evaluation

Implemented a retrieval system using cosine similarity.

When a user asks a question:

1. The question is converted into an embedding.
2. Its embedding is compared with stored document embeddings.
3. The three most similar chunks are retrieved.
4. The retrieved context is passed to the LLM.
5. The LLM generates an answer using the retrieved context.

If the answer is not available in the context, the model is instructed to respond with "I don't know".

Used `qwen3.5:2b` through Ollama for answer generation.

Required model:

```bash
ollama pull qwen3.5:2b
```

Run:

```bash
uv run python rag_lab/retrieval.py
```


### Evaluation Results

Tested the retrieval system using 10 questions with known expected source documents.

Recall@3 measures whether the expected document appears among the top three retrieved chunks.

| Chunking Strategy | Correct Retrievals | Recall@3 |
|-------------------|--------------------|----------|
| Fixed-size        | 10/10              | 100%     |
| Sentence-based    | 10/10              | 100%     |
| Paragraph-based   | 10/10              | 100%     |

All three strategies achieved 100% Recall@3 in this experiment. Therefore, no single strategy performed better based on this metric.

The evaluation results are saved in:
```
    rag_lab/results/evaluation.json
```


## 7. What an LLM Cannot Do

Prepared a short customer-facing document explaining the limitations of LLMs.

The document covers:
- Incorrect or hallucinated answers
- Limitations of up-to-date information
- Lack of human understanding and experience
- Restricted access to private information
- The need for human review

It also includes an example comparing a small local model with a larger hosted model.

## 8. AI Building Blocks Map

Prepared a summary of seven important AI building blocks:

1. Multimodal Input
2. Fine-Tuning
3. Multi-Agent Systems
4. Memory
5. Context Management
6. AI Gateways
7. Skills

For each building block, the summary explains what it is, when to use it and its possible costs or risks.

## Key Learnings

During this assignment, I learned:

- How tokenizers count tokens in different types of text.
- How to generate synthetic documents and split them into chunks.
- How embeddings represent text as numerical vectors.
- How cosine similarity helps retrieve relevant information.
- How to build a basic RAG pipeline using a local LLM.
- How to evaluate retrieval quality using Recall@3.
- Why different chunking strategies can affect retrieval results.
- Why LLM answers need proper context and human verification.

## Conclusion

This assignment helped me understand how a basic RAG application works, from preparing documents to retrieving relevant information and generating answers. I also learned that choosing the right models, managing context and evaluating retrieval quality are important when building reliable AI applications.