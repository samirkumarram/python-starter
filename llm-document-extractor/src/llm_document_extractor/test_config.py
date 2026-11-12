from llm_document_extractor.config import load_settings


def test_load_settings():
    settings = load_settings()

    assert settings.model.provider == "groq"
    assert settings.model.model == "openai/gpt-oss-20b"
    assert settings.model.base_url == "https://api.groq.com/openai/v1"
    assert settings.model.api_key_env == "GROQ_API_KEY"
    assert settings.timeout_seconds == 60
    assert settings.max_retries == 2
