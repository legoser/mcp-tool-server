import re

import httpx
from bs4 import BeautifulSoup

from ..core.logging import get_logger
from .rate_limiter import RateLimiter

logger = get_logger(__name__)

DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


class WebFetcher:
    def __init__(self) -> None:
        self.rate_limiter = RateLimiter(requests_per_minute=20)
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None:
            self._client = httpx.AsyncClient(
                timeout=30.0,
                follow_redirects=True,
                headers=DEFAULT_HEADERS,
            )
        return self._client

    async def close(self) -> None:
        if self._client:
            await self._client.aclose()
            self._client = None

    async def fetch(self, url: str) -> str:
        await self.rate_limiter.acquire()

        try:
            client = await self._get_client()
            response = await client.get(url)
            response.raise_for_status()
        except httpx.TimeoutException:
            return "Ошибка: время ожидания истекло"
        except httpx.HTTPError as e:
            return f"Ошибка HTTP: {str(e)}"
        except Exception as e:
            return f"Ошибка при загрузке: {str(e)}"

        content_type = response.headers.get("content-type", "")

        if "text/html" in content_type:
            soup = BeautifulSoup(response.text, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            title = soup.title.string if soup.title else "Без заголовка"

            text = soup.get_text(separator="\n", strip=True)
            text = re.sub(r"\n{3,}", "\n\n", text)
            text = re.sub(r" {2,}", " ", text)

            max_length = 8000
            if len(text) > max_length:
                text = text[:max_length] + "\n\n... (текст обрезан)"

            return f"Заголовок: {title}\n\nURL: {url}\n\nСодержимое:\n{text}"

        return f"URL: {url}\n\nТип контента: {content_type}\n\n{response.text[:5000]}"


_fetcher: WebFetcher | None = None


async def get_fetcher() -> WebFetcher:
    global _fetcher
    if _fetcher is None:
        _fetcher = WebFetcher()
    return _fetcher
