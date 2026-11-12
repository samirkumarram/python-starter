from typing import TypeVar
from pydantic import BaseModel, ValidationError

from llm_document_extractor.llm_client import LLMClient
from llm_document_extractor.prompt_manager import PromptManager

T = TypeVar("T", bound=BaseModel)

class DocumentExtractor:
    def __init__(self, llm_client: LLMClient, prompt_manager: PromptManager):
        self.llm_client = llm_client
        self.prompt_manager = prompt_manager

    def extract(self, document_type: str, document_text: str) -> str:
        system_prompt = self.prompt_manager.get_system_prompt(document_type)
        extraction_prompt = self.prompt_manager.get_extraction_prompt(document_type)
        user_prompt = (f"{extraction_prompt}\n\n"
                       "DOCUMENT TEXT:\n"
                       f"{document_text}")
        print("\n========== PROMPT SENT TO MODEL ==========")
        print(user_prompt)
        print("==========================================\n")
        return self.llm_client.generate(prompt=user_prompt, system_prompt=system_prompt)

    def extract_structured(self, document_type: str, document_text: str, response_model: type[T],) -> T:
        system_prompt = self.prompt_manager.get_system_prompt(document_type)
        extraction_prompt = self.prompt_manager.get_extraction_prompt(document_type)

        user_prompt = f"{extraction_prompt}\n\nDOCUMENT TEXT:\n{document_text}"

        print("\n========== PROMPT SENT TO MODEL ==========")
        print(user_prompt)
        print("==========================================\n")

        response = self.llm_client.generate(
            prompt=user_prompt,
            system_prompt=system_prompt,
        )

        try:
            return response_model.model_validate_json(response)

        except ValidationError as error:
            repair_prompt = (
                f"{user_prompt}\n\n"
                "Your previous response was invalid. "
                "Correct the response so it satisfies the required schema.\n\n"
                f"Validation error:\n{error}\n\n"
                f"Previous response:\n{response}\n\n"
                "Return only valid JSON. Do not include explanations."
            )

            repaired_response = self.llm_client.generate(
                prompt=repair_prompt,
                system_prompt=system_prompt,
            )

            return response_model.model_validate_json(repaired_response)