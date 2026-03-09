from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    BASE_URL: str = "http://0.0.0.0:3344"

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 3344

    OPENAI_BASE_URL: str = "http://192.168.57.139:11434/v1"
    OPENAI_API_KEY: str = "ollama"
    LLM_MODEL_NAME: str = "qwen2.5-coder:7b"
    LLM_AVAILABLE_MODELS: list[str] = [
        "llama3",
        "llama3.1",
        "llama3.2",
        "qwen3",
        "qwen2.5-coder:7b",
        "mistral",
    ]

    BRAVE_API_KEY: str = ""

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


settings = Settings()
