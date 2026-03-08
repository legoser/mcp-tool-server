from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )

    client_token: str = ""
    client_base_url: str = "http://localhost:3344"

    openai_base_url: str = "http://192.168.57.139:11434/v1"
    openai_api_key: str = "ollama"
    llm_model_name: str = "qwen2.5-coder:7b"
    llm_available_models: list[str] = [
        "llama3",
        "llama3.1",
        "llama3.2",
        "qwen3",
        "qwen2.5-coder:7b",
        "mistral",
    ]

    brave_api_key: str = ""

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


settings = Settings()
