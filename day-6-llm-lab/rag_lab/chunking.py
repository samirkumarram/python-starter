
from pathlib import Path
import json
import re

DOCUMENT_DIR = Path("rag_lab/documents")
OUTPUT_DIR = Path("rag_lab/chunks")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def fixed_size_chunk(text, chunk_size=50):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]


def sentence_based_chunk(text, sentences_per_chunk=2):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    return [
        " ".join(sentences[i:i + sentences_per_chunk])
        for i in range(0, len(sentences), sentences_per_chunk)
    ]


def paragraph_based_chunk(text):
    return [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]


strategies = {
    "fixed_size": fixed_size_chunk,
    "sentence_based": sentence_based_chunk,
    "paragraph_based": paragraph_based_chunk
}


all_results = {}

for strategy_name, chunk_function in strategies.items():

    strategy_chunks = []

    for document_path in sorted(DOCUMENT_DIR.glob("*.txt")):

        text = document_path.read_text(encoding="utf-8")

        chunks = chunk_function(text)

        for index, chunk in enumerate(chunks):
            strategy_chunks.append({
                "document": document_path.name,
                "chunk_id": index,
                "text": chunk
            })

    all_results[strategy_name] = strategy_chunks

    output_file = OUTPUT_DIR / f"{strategy_name}.json"

    output_file.write_text(
        json.dumps(strategy_chunks, indent=4, ensure_ascii=False),
        encoding="utf-8"
    )

    print(
        f"{strategy_name}: "
        f"{len(strategy_chunks)} chunks generated"
    )
