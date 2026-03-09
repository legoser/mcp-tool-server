from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 3344
    TRANSPORT: str = "http"
    FASTMCP_STATELESS_HTTP: bool = True
    CLIENT_TOKEN: str = ""
    CLIENT_BASE_URL: str = "http://localhost:3344"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"

    # HTTP client settings
    HTTP_TIMEOUT: float = 30.0
    HTTP_VERIFY_SSL: bool = True

    # Rate limiting
    SEARCH_RATE_LIMIT: int = 30
    WEB_FETCH_RATE_LIMIT: int = 20
    WEATHER_RATE_LIMIT: int = 30
    WEATHER_DAYS_LIMIT: int = 21

    # Ollama / LLM settings
    OPENAI_BASE_URL: str = "http://localhost:11434/v1"
    OPENAI_API_KEY: str = "ollama"
    LLM_MODEL_NAME: str = "qwen2.5-coder:7b"
    LLM_AVAILABLE_MODELS: list[str] = [
        "llama3",
        "llama3.1",
        "llama3.2",
        "qwen2.5-coder:7b",
        "mistral",
    ]

    # Search providers API keys
    BRAVE_API_KEY: str = ""

    # Weather API (Open-Meteo - free, no key required)
    WEATHER_API_GEOCODING_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    WEATHER_API_FORECAST_URL: str = "https://api.open-meteo.com/v1/forecast"

    # Web fetch settings
    WEB_FETCH_MAX_LENGTH: int = 8000


settings = Settings()
