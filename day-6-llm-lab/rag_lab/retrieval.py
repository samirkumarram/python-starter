from pathlib import Path
import json
import urllib.request
import math

DB_DIR = Path("rag_lab/vector_db")
OUTPUT_DIR = Path("rag_lab/results")

OUTPUT_DIR.mkdir(parents = True, exist_ok = True)

EMBED_URL = "http://localhost:11434/api/embed"
CHAT_URL = "http://localhost:11434/api/chat"

EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3.5:2b"

TOP_K = 3

questions = [
    {
        "question": "How many paid leave days do employees receive annually?",
        "expected": "policy_01.txt"
    },
    {
        "question": "How many days per week can employees work from home?",
        "expected": "policy_02.txt"
    },
    {
        "question": "What is the minimum password length?",
        "expected": "policy_03.txt"
    },
    {
        "question": "How many working hours must employees complete daily?",
        "expected": "policy_05.txt"
    },
    {
        "question": "Is multi-factor authentication required for remote access?",
        "expected": "policy_06.txt"
    },
    {
        "question": "Within how many minutes must security incidents be reported?",
        "expected": "policy_09.txt"
    },
    {
        "question": "How long must customer transaction records be retained?",
        "expected": "policy_10.txt"
    },
    {
        "question": "How often must critical business databases be backed up?",
        "expected": "policy_13.txt"
    },
    {
        "question": "What is the maximum recovery time for critical business applications?",
        "expected": "policy_14.txt"
    },
    {
        "question": "When must IT revoke system access after an employee leaves?",
        "expected": "policy_20.txt"
    }
]

def get_embedding(text):
    payload = {
        "model": EMBED_MODEL,
        "input": "search_query: " + text
    }

    request = urllib.request.Request(
        EMBED_URL,
        data = json.dumps(payload).encode(),
        headers = {"Content-Type": "application/json"},
        method = "POST"
    )
    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode())
    return result["embeddings"][0]

def cosine_similarity(vector_a, vector_b):
    dot_product = sum(
        a * b for a, b in zip(vector_a, vector_b)
    )

    magnitude_a = math.sqrt(sum(a * a for a in vector_a))
    magnitude_b = math.sqrt(sum(b * b for b in vector_b))

    if magnitude_a == 0 or magnitude_b == 0:
        return 0

    return dot_product / (magnitude_a * magnitude_b)

def retrieve(question, vectors):
    query_embedding = get_embedding(question)

    scored_chunks = []

    for chunk in vectors:
        score = cosine_similarity(
            query_embedding,
            chunk["embedding"]
        )

        scored_chunks.append({
            "document": chunk["document"],
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "similarity": score
        })

    scored_chunks.sort(
        key=lambda item: item["similarity"],
        reverse=True
    )

    print(f"\nDEBUG QUESTION: {question}")

    for chunk in scored_chunks[:TOP_K]:
        print(
            f"DEBUG: {chunk['document']} "
            f"| Score: {chunk['similarity']:.6f}"
        )
    return scored_chunks[:TOP_K]


def generate_answer(question, retrieved_chunks):
    context = "\n\n".join(
        chunk["text"] for chunk in retrieved_chunks
    )

    prompt = f"""
        Answer the question using only the provided context.
        If the answer is not available in the context, say "I don't know".

        Question:
        {question}

        Context:
        {context}
    """

    payload = {
        "model": CHAT_MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "stream": False
    }

    request = urllib.request.Request(
        CHAT_URL,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        result = json.loads(response.read().decode())

    return result["message"]["content"]


strategies = [
    "fixed_size",
    "sentence_based",
    "paragraph_based"
]

all_results = {}

for strategy in strategies:

    input_file = DB_DIR / f"{strategy}.json"

    vectors = json.loads(
        input_file.read_text(encoding="utf-8")
    )

    strategy_results = []
    correct_retrievals = 0

    print(f"\n===== {strategy} =====")

    for item in questions:

        question = item["question"]
        expected = item["expected"]

        top_chunks = retrieve(question, vectors)

        # Check whether the expected document appears in top 3
        found = any(
            chunk["document"] == expected
            for chunk in top_chunks
        )

        if found:
            correct_retrievals += 1

        answer = generate_answer(question, top_chunks)

        result = {
            "question": question,
            "expected_document": expected,
            "retrieved_chunks": top_chunks,
            "retrieval_success": found,
            "answer": answer
        }

        strategy_results.append(result)

        print(f"\nQuestion: {question}")
        print(f"Expected document: {expected}")
        print(f"Retrieved documents: "
              f"{[c['document'] for c in top_chunks]}")
        print(f"Answer: {answer}")

    recall = correct_retrievals / len(questions)

    all_results[strategy] = {
        "recall_at_3": recall,
        "correct_retrievals": correct_retrievals,
        "total_questions": len(questions),
        "results": strategy_results
    }

    print(
        f"\nRecall@3: {correct_retrievals}/10 "
        f"({recall * 100:.1f}%)"
    )

output_file = OUTPUT_DIR / "evaluation.json"

output_file.write_text(
    json.dumps(all_results, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print("\nEvaluation completed.")
print(f"Results saved to: {output_file}")
