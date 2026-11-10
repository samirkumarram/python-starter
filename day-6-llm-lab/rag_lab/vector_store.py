from pathlib import Path
import json

EMBEDDING_DIR = Path("rag_lab/embeddings")
DB_DIR = Path("rag_lab/vector_db")

DB_DIR.mkdir(parents = True, exist_ok = True)

strategies = ["fixed_size", "sentence_based", "paragraph_based"]
for strategy in strategies:
    input_file = EMBEDDING_DIR / f"{strategy}.json"
    chunks = json.loads(input_file.read_text(encoding = "utf-8"))
    
    vectors = []

    for chunk in chunks:
        vectors.append({
            "id": f"{chunk['document']}_{chunk['chunk_id']}",
            "document": chunk["document"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "embedding": chunk["embedding"]
        })
    
    output_file = DB_DIR / f"{strategy}.json"
    output_file.write_text(json.dumps(vectors, ensure_ascii = False), encoding = "utf-8")
    print(f"{strategy}: " f"{len(vectors)} vectors stored")
print("Vector database creation completed.")