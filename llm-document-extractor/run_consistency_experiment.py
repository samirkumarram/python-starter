
import os
import time
from pathlib import Path

from openai import OpenAI

from llm_document_extractor.config import load_settings
from llm_document_extractor.prompt_manager import PromptManager


# 1. Load the existing project settings.
settings = load_settings()

# 2. Create the Ollama client.
api_key = os.getenv(settings.model.api_key_env) or "ollama"

client = OpenAI(
    base_url=settings.model.base_url,
    api_key=api_key,
    timeout=180,
)

# 3. Load the same CV and prompts for every experiment.
project_root = Path(__file__).resolve().parent

cv_path = project_root / "day5_samples" / "cvs" / "cv_01.txt"
document_text = cv_path.read_text(encoding="utf-8")

prompt_manager = PromptManager()

system_prompt = prompt_manager.get_system_prompt("cv")
extraction_prompt = prompt_manager.get_extraction_prompt("cv")

user_prompt = (
    f"{extraction_prompt}\n\n"
    "DOCUMENT TEXT:\n"
    f"{document_text}"
)

# 4. Define the seven experiments.
experiments = [
    ("Temperature 0 - Run 1", 0, None),
    ("Temperature 0 - Run 2", 0, None),
    ("Temperature 0 - Run 3", 0, None),
    ("Temperature 0.8 - Run 1", 0.8, None),
    ("Temperature 0.8 - Run 2", 0.8, None),
    ("Temperature 0.8 - Run 3", 0.8, None),
    ("Fixed seed 42", 0.8, 42),
]

# 5. Store experiment outputs.
results_dir = project_root / "experiments"
results_dir.mkdir(exist_ok=True)

results_file = results_dir / "consistency_results.txt"

with results_file.open("w", encoding="utf-8") as file:
    for name, temperature, seed in experiments:
        print(f"\n========== {name} ==========")

        request_options = {
            "model": settings.model.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": settings.max_tokens,
            "extra_body": {"reasoning_effort": "none"},
        }

        if seed is not None:
            request_options["seed"] = seed

        start_time = time.perf_counter()

        response = client.chat.completions.create(**request_options)

        elapsed_time = time.perf_counter() - start_time
        output = response.choices[0].message.content or ""

        print(f"Time taken: {elapsed_time:.2f} seconds")
        print(output)

        file.write(f"\n========== {name} ==========\n")
        file.write(f"Temperature: {temperature}\n")
        file.write(f"Seed: {seed}\n")
        file.write(f"Time: {elapsed_time:.2f} seconds\n")
        file.write(output + "\n")

print("\nAll seven experiments completed.")
print(f"Results saved in: {results_file}")
