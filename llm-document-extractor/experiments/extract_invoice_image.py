
import base64
import json
from pathlib import Path

from openai import OpenAI

from llm_document_extractor.config import load_settings
from llm_document_extractor.schemas import InvoiceData

# 1. Load project settings.
settings = load_settings()

# 2. Create the Ollama client.
client = OpenAI(
    base_url=settings.model.base_url,
    api_key="ollama",
    timeout=180,
)

# 3. Locate the invoice image.
project_root = Path(__file__).resolve().parents[1]
image_path = project_root / "day5_samples" / "invoice_image" / "invoice.png"

# 4. Convert the image into Base64 format.
with image_path.open("rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# 5. Load the versioned invoice prompts.
system_prompt = (
    project_root / "prompts" / "invoice" / "v1" / "system.txt"
).read_text(encoding="utf-8")

extraction_prompt = (
    project_root / "prompts" / "invoice" / "v1" / "extraction.txt"
).read_text(encoding="utf-8")

user_prompt = (
    extraction_prompt
    + "\n\nThe invoice is attached as an image. "
    "Extract the requested fields and return only valid JSON."
)

# 6. Send the image and prompts to the vision model.
print("Starting invoice image extraction...")

response = client.chat.completions.create(
    model=settings.model.model,
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_prompt},
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{encoded_image}",
                        "detail": "high",
                    },
                },
            ],
        },
    ],
    temperature=0,
    max_tokens=1500,
    extra_body={"reasoning_effort": "none"},
)

# 7. Get the model response.
output = response.choices[0].message.content or ""

print("\nRaw model response:")
print(output)

# 8. Remove Markdown code fences if the model includes them.
cleaned_output = output.strip()

if cleaned_output.startswith("```"):
    cleaned_output = cleaned_output.removeprefix("```json")
    cleaned_output = cleaned_output.removeprefix("```")
    cleaned_output = cleaned_output.removesuffix("```")
    cleaned_output = cleaned_output.strip()

# 9. Validate the response using Pydantic.
invoice = InvoiceData.model_validate_json(cleaned_output)
# 10. Display the validated invoice data.
print("\nValidated invoice data:")
print(invoice.model_dump_json(indent=4))

# 10. Display the validated invoice data.
print("\nValidated invoice data:")
print(invoice.model_dump_json(indent=4))

# 11. Save the validated result.
output_path = project_root / "experiments" / "invoice_image_result.json"

output_path.write_text(
    invoice.model_dump_json(indent=4),
    encoding="utf-8",
)

print(f"\nResult saved to: {output_path}")
