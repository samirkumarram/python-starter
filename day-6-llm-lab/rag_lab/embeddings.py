
from pathlib import Path
import json
import urllib.request

CHUNK_DIR = Path("rag_lab/chunks")
OUTPUT_DIR = Path("rag_lab/embeddings")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "nomic-embed-text"
API_URL = "http://localhost:11434/api/embed"


def generate_embeddings(texts):
    payload = {
        "model": MODEL,
        "input": texts
    }

    request = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["embeddings"]


# Process all three chunking strategies
for chunk_file in sorted(CHUNK_DIR.glob("*.json")):

    chunks = json.loads(
        chunk_file.read_text(encoding="utf-8")
    )

    texts = ["search_document: " + chunk["text"] for chunk in chunks]

    embedded_chunks = []

    # Process in batches of 32
    for start in range(0, len(texts), 32):

        batch = texts[start:start + 32]

        embeddings = generate_embeddings(batch)

        for chunk, embedding in zip(
            chunks[start:start + 32],
            embeddings
        ):
            embedded_chunks.append({
                **chunk,
                "embedding": embedding
            })

    output_file = OUTPUT_DIR / chunk_file.name

    output_file.write_text(
        json.dumps(embedded_chunks, indent=2),
        encoding="utf-8"
    )

    print(
        f"{chunk_file.stem}: "
        f"{len(embedded_chunks)} embeddings generated"
    )

print("Embedding generation completed.")
