import os
from openai import(
    APIConnectionError,
    APIError,
    APITimeoutError,
    InternalServerError,
    OpenAI,
    RateLimitError
)
from tenacity import(Retrying, retry_if_exception_type, stop_after_attempt, wait_exponential)
from llm_document_extractor.config import Settings

class LLMClient:
    def __init__(self, settings: Settings):
        self.settings = settings
        api_key = os.getenv(settings.model.api_key_env)
        if not api_key and settings.model.provider.lower() == "ollama":
            api_key = "ollama"
        if not api_key:
            raise ValueError(f"API key environment variable "
                             f"{settings.model.api_key_env} is not set.")
        self.client = OpenAI(
            base_url=settings.model.base_url,
            api_key=api_key,
            timeout=settings.timeout_seconds
        )
    def _request_model(self, model: str, messages: list[dict[str, str]]) -> str:
        retryer = Retrying(
            stop=stop_after_attempt(self.settings.max_retries + 1),
            wait=wait_exponential(multiplier=1, min=1,max=10),
            retry= retry_if_exception_type(
                (
                    APIConnectionError,
                    APITimeoutError,
                    RateLimitError,
                    InternalServerError
                )
            ),
            reraise = True
        )
        for attempt in retryer:
            with attempt:
                request_options = {
                    "model": model,
                    "messages": messages,
                    "temperature": self.settings.temperature,
                    "max_tokens": self.settings.max_tokens,
                }

                if self.settings.model.provider.lower() == "ollama":
                    request_options["extra_body"] = {"reasoning_effort": "none"}

                response = self.client.chat.completions.create(**request_options)
                content = response.choices[0].message.content

                usage = getattr(response, "usage", None)

                if usage is not None:
                    print(f"Input tokens: {usage.prompt_tokens}")
                    print(f"Output tokens: {usage.completion_tokens}")
                    print(f"Total tokens: {usage.total_tokens}")

                if content is None:
                    raise ValueError("The LLM returned an empty response.")
                print("\n========== RAW MODEL RESPONSE ==========")
                print(repr(content))
                print("========================================\n")
                return content
        raise RuntimeError("LLM request failed.")
    def generate(self, prompt: str, system_prompt: str = "You are a helpul assistant.") -> str:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
        models = [
            self.settings.model.model,
            *self.settings.model.fallback_models
        ]
        last_error = None
        for model in models:
            try:
                return self._request_model(model, messages)
            except APIError as error:
                last_error = error
        raise RuntimeError("All configured LLM models failed.") from last_error