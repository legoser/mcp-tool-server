from ..core.config import settings
from ..core.logging import get_logger
from ..mcp import mcp
from ..utils.http_client import get_http_client

logger = get_logger(__name__)


@mcp.tool()
async def generate_text(prompt: str) -> str:
    """Генерирует текст с использованием локальной модели Ollama."""
    client = await get_http_client()

    payload = {
        "model": settings.LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    resp = await client.post(
        f"{settings.OPENAI_BASE_URL}/completions",
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["text"].strip()


@mcp.tool()
async def chat_with_ai(system_prompt: str, user_message: str) -> str:
    """Отправляет сообщение в чат с локальной моделью Ollama."""
    client = await get_http_client()

    payload = {
        "model": settings.LLM_MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        "stream": False,
    }

    resp = await client.post(
        f"{settings.OPENAI_BASE_URL}/chat/completions",
        json=payload,
    )
    resp.raise_for_status()
    data = resp.json()
    return data["choices"][0]["message"]["content"].strip()


@mcp.tool()
async def list_ollama_models() -> str:
    """Возвращает список доступных моделей в Ollama.

    По умолчанию доступны: llama3, llama3.1, llama3.2, qwen2.5, mistral
    """
    client = await get_http_client()

    resp = await client.get(f"{settings.OPENAI_BASE_URL.replace('/v1', '')}/api/tags")
    resp.raise_for_status()
    data = resp.json()

    models = [m["name"] for m in data.get("models", [])]
    if not models:
        return "Нет доступных моделей"

    return "Доступные модели:\n" + "\n".join(f"- {m}" for m in models)
