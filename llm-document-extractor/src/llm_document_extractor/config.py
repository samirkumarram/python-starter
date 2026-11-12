from pathlib import Path
import yaml
from pydantic import BaseModel, Field

class ModelSettings(BaseModel):
    provider: str
    base_url: str
    model: str
    api_key_env: str = "OPENAI_API_KEY"
    fallback_models: list[str] = Field(default_factory = list)

class Settings(BaseModel):
    model: ModelSettings
    timeout_seconds: float = Field(default = 30.0, gt = 0)
    max_retries: int = Field(default = 2, ge = 0)
    temperature: float = Field(default = 0.0, ge = 0.0, le = 2)
    max_tokens: int = Field(default = 1500, gt = 0)

def load_settings() -> Settings:
    project_root = Path(__file__).resolve().parents[2]
    config_path = project_root / "config" / "settings.yaml"
    with config_path.open("r", encoding = "utf-8") as file:
        config_data = yaml.safe_load(file)

    if not isinstance(config_data, dict):
        raise ValueError("Settings file must contain a YAML mapping.")
    return Settings(**config_data)