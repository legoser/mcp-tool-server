
from ..core.logging import get_logger
from ..utils.http_client import get_http_client

logger = get_logger(__name__)


async def get_random_joke() -> str:
    """Возвращает случайный анекдот/шутку на английском языке."""
    client = await get_http_client()
    resp = await client.get("https://official-joke-api.appspot.com/random_joke")
    resp.raise_for_status()
    data = resp.json()
    return f"{data['setup']}\n— {data['punchline']}"


async def get_random_quote() -> str:
    """Возвращает случайную вдохновляющую цитату."""
    client = await get_http_client()
    resp = await client.get("https://zenquotes.io/api/random")
    resp.raise_for_status()
    data = resp.json()[0]
    return f"«{data['q']}»\n— {data['a']}"


async def get_random_fact() -> str:
    """Возвращает случайный интересный факт на английском языке."""
    client = await get_http_client()
    resp = await client.get("https://uselessfacts.jsph.pl/api/v2/facts/random?language=en")
    resp.raise_for_status()
    data = resp.json()
    return data["text"]
