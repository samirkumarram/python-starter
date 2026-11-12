import time
from pathlib import Path

from openai import OpenAI

from llm_document_extractor.config import load_settings
from llm_document_extractor.prompt_manager import PromptManager

settings = load_settings()

client = OpenAI(
    base_url=settings.model.base_url,
    api_key="ollama",
    timeout=600,
)

project_root = Path(__file__).resolve().parents[1]

document = (
    project_root / "experiments" / "long_document_large.txt"
).read_text(encoding="utf-8")

prompts = PromptManager()
system_prompt = prompts.get_system_prompt("cv")
extraction_prompt = prompts.get_extraction_prompt("cv")

user_prompt = (
    f"{extraction_prompt}\n\n"
    "DOCUMENT TEXT:\n"
    f"{document}"
)

print("Starting long-document extraction...")
print(f"Document words: {len(document.split())}")

start = time.perf_counter()

response = client.chat.completions.create(
    model="qwen3.5-2b-ctx8k",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    temperature=0,
    max_tokens=1500,
    extra_body={"reasoning_effort": "none"},
)

elapsed = time.perf_counter() - start
output = response.choices[0].message.content or ""

print(f"\nTime taken: {elapsed:.2f} seconds")
print("\nModel response:")
print(output)

output_path = project_root / "experiments" / "context_8192_result.txt"
output_path.write_text(output, encoding="utf-8")

print(f"\nSaved result to: {output_path}")