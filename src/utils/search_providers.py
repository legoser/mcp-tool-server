import urllib.parse
from typing import Any

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


class DuckDuckGoProvider:
    name = "DuckDuckGo"

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, Any]]:
        client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        try:
            search_url = "https://api.duckduckgo.com/"
            params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
            headers = {"User-Agent": DEFAULT_HEADERS["User-Agent"]}

            resp = await client.get(search_url, params=params, headers=headers)

            if resp.status_code not in (200, 202):
                logger.warning(f"DuckDuckGo error: status {resp.status_code}")
                return []

            data = resp.json()
            results = []

            if data.get("AbstractText"):
                results.append(
                    {
                        "title": data.get("Heading", "Result"),
                        "url": data.get("AbstractURL", ""),
                        "snippet": data["AbstractText"],
                    }
                )

            if "RelatedTopics" in data:
                for item in data["RelatedTopics"]:
                    if len(results) >= num_results:
                        break
                    if "FirstURL" in item and "Text" in item:
                        text = item["Text"]
                        results.append(
                            {
                                "title": text.split(" - ")[0] if " - " in text else text[:50],
                                "url": item["FirstURL"],
                                "snippet": text,
                            }
                        )
                    elif "Topics" in item:
                        for topic in item["Topics"]:
                            if len(results) >= num_results:
                                break
                            if "FirstURL" in topic and "Text" in topic:
                                text = topic["Text"]
                                results.append(
                                    {
                                        "title": text.split(" - ")[0]
                                        if " - " in text
                                        else text[:50],
                                        "url": topic["FirstURL"],
                                        "snippet": text,
                                    }
                                )

            return results
        except Exception as e:
            logger.warning(f"DuckDuckGo exception: {e}")
            return []
        finally:
            await client.aclose()


class DuckDuckGoHTMLProvider:
    name = "DuckDuckGo HTML"
    BASE_URL = "https://html.duckduckgo.com/html"

    def __init__(self) -> None:
        from ..core.config import settings

        self.rate_limiter = RateLimiter(requests_per_minute=settings.SEARCH_RATE_LIMIT)
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

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, Any]]:
        await self.rate_limiter.acquire()

        data = {"q": query, "b": "", "kl": ""}

        try:
            client = await self._get_client()
            response = await client.post(self.BASE_URL, data=data)
            response.raise_for_status()
        except httpx.TimeoutException:
            logger.error("Search request timed out")
            return []
        except httpx.HTTPError as e:
            logger.error(f"HTTP error during search: {e}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error during search: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        results = []

        for result in soup.select(".result"):
            if len(results) >= num_results:
                break

            title_elem = result.select_one(".result__title")
            if not title_elem:
                continue

            link_elem = title_elem.find("a")
            if not link_elem:
                continue

            title = link_elem.get_text(strip=True)
            link = str(link_elem.get("href") or "")

            if "y.js" in link:
                continue

            if link.startswith("//duckduckgo.com/l/?uddg="):
                link = urllib.parse.unquote(link.split("uddg=")[1].split("&")[0])

            snippet_elem = result.select_one(".result__snippet")
            snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

            results.append(
                {
                    "title": title,
                    "url": link,
                    "snippet": snippet,
                }
            )

        logger.info(f"DuckDuckGo returned {len(results)} results for: {query}")
        return results


class BraveSearchProvider:
    name = "Brave Search"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, Any]]:
        client = httpx.AsyncClient(timeout=30.0, follow_redirects=True)
        headers = {
            "User-Agent": DEFAULT_HEADERS["User-Agent"],
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-Subscription-Token"] = self.api_key

        try:
            search_url = "https://api.search.brave.com/res/v1/web/search"
            params = {"q": query, "count": min(num_results, 20)}

            resp = await client.get(search_url, params=params, headers=headers)

            if resp.status_code == 401:
                logger.warning("Brave Search: invalid API key")
                return []
            if resp.status_code != 200:
                logger.warning(f"Brave Search error: status {resp.status_code}")
                return []

            data = resp.json()
            results = []

            web_results = data.get("web", {}).get("results", [])
            for item in web_results[:num_results]:
                results.append(
                    {
                        "title": item.get("title", ""),
                        "url": item.get("url", ""),
                        "snippet": item.get("description", ""),
                    }
                )

            return results
        except Exception as e:
            logger.warning(f"Brave Search exception: {e}")
            return []
        finally:
            await client.aclose()


_ddg_html_provider: DuckDuckGoHTMLProvider | None = None


async def get_ddg_html_provider() -> DuckDuckGoHTMLProvider:
    """Get singleton DDG HTML provider with rate limiting."""
    global _ddg_html_provider
    if _ddg_html_provider is None:
        _ddg_html_provider = DuckDuckGoHTMLProvider()
    return _ddg_html_provider


async def search_with_fallback(query: str, num_results: int = 5) -> list[dict[str, Any]]:
    """Search with fallback: DDG HTML (rate limited) → DDG API → Brave."""
    from ..core.config import settings

    ddg_html = await get_ddg_html_provider()
    providers: list = [
        ddg_html,
        DuckDuckGoProvider(),
        BraveSearchProvider(api_key=settings.BRAVE_API_KEY or None),
    ]

    for provider in providers:
        provider_name = getattr(provider, "name", provider.__class__.__name__)
        logger.info(f"Trying search provider: {provider_name}")
        results = await provider.search(query, num_results)
        if results:
            logger.info(f"{provider_name} returned {len(results)} results")
            return results
        logger.warning(f"{provider_name} returned no results")

    return []
