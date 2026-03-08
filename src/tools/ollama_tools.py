from ..core.config import settings
from ..core.logging import get_logger
from ..utils.http_client import get_http_client

logger = get_logger(__name__)


async def generate_text(prompt: str) -> str:
    """Генерирует текст с использованием локальной модели Ollama."""
    client = await get_http_client()

    payload = {
        "model": settings.llm_model_name,
        "prompt": prompt,
        "stream": False,
    }

    resp = await client.post(
        f"{settings.openai_base_url}/completions",
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["text"].strip()


async def chat_with_ai(system_prompt: str, user_message: str) -> str:
    """Отправляет сообщение в чат с локальной моделью Ollama."""
    client = await get_http_client()

    payload = {
        "model": settings.llm_model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    resp = await client.post(
        f"{settings.openai_base_url}/chat/completions",
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


async def list_ollama_models() -> str:
    """Возвращает список доступных моделей в Ollama.

    По умолчанию доступны: llama3, llama3.1, llama3.2, qwen2.5, mistral
    """
    client = await get_http_client()

    resp = await client.get(f"{settings.openai_base_url.replace('/v1', '')}/api/tags")
    resp.raise_for_status()
    data = resp.json()

    models = [m["name"] for m in data.get("models", [])]
    if not models:
        return "Нет доступных моделей"

    return "Доступные модели:\n" + "\n".join(f"- {m}" for m in models)
