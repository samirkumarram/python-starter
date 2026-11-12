from types import SimpleNamespace
from unittest.mock import Mock

import httpx
import pytest
from openai import APIConnectionError

from llm_document_extractor.config import ModelSettings, Settings
from llm_document_extractor.llm_client import LLMClient

def create_settings() -> Settings:
    return Settings(
        model=ModelSettings(
            provider="ollama",
            base_url="http://localhost:11434/v1",
            model="qwen3.5:2b",
            fallback_models=["qwen2.5:3b"]
        )
    )

def test_successful_llm_response(monkeypatch):
    mock_openai = Mock()

    mock_openai.return_value.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content="Hello from Ollama"))
            ]
        )
    )

    monkeypatch.setattr("llm_document_extractor.llm_client.OpenAI", mock_openai)
    client = LLMClient(create_settings())
    result = client.generate("Say Hello")
    assert result == "Hello from Ollama"

def test_correct_model_selection(monkeypatch):
    mock_openai = Mock()
    mock_openai.return_value.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content="Test response")
                )
            ]
        )
    )
    monkeypatch.setattr("llm_document_extractor.llm_client.OpenAI", mock_openai)
    client = LLMClient(create_settings())
    client.generate("Test prompt")
    mock_openai.return_value.chat.completions.create.assert_called_once()
    call_kwargs = (mock_openai.return_value.chat.completions.create.call_args.kwargs)
    assert call_kwargs["model"] == "qwen3.5:2b"

def test_fallback_model_selection(monkeypatch):
    monkeypatch.setattr("llm_document_extractor.llm_client.OpenAI", Mock())
    client = LLMClient(create_settings())

    mock_request = Mock(
        side_effect=[
            APIConnectionError(request=httpx.Request("POST", "http://localhost")),
            "Fallback response"
        ]
    )
    monkeypatch.setattr(client, "_request_model", mock_request)
    result = client.generate("Test prompt")
    assert result == "Fallback response"
    assert mock_request.call_args_list[0].args[0] == "qwen3.5:2b"
    assert mock_request.call_args_list[1].args[0] == "qwen2.5:3b"

def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    settings = create_settings()
    settings.model.provider = "openai"
    with pytest.raises(ValueError, match="API key environment variable"):
        LLMClient(settings)

def test_empty_llm_response(monkeypatch):
    mock_openai = Mock()
    mock_openai.return_value.chat.completions.create.return_value = (
        SimpleNamespace(
            choices=[
                SimpleNamespace(message=SimpleNamespace(content=None))
            ]
        )
    )
    monkeypatch.setattr("llm_document_extractor.llm_client.OpenAI", mock_openai)
    client = LLMClient(create_settings())
    with pytest.raises(ValueError, match="empty response"):
        client.generate("Test prompt")