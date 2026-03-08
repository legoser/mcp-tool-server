from typing import Protocol

from bs4 import BeautifulSoup

from ..core.logging import get_logger

logger = get_logger(__name__)


class SearchProvider(Protocol):
    async def search(self, query: str, num_results: int) -> list[dict[str, str]]: ...


def get_provider_name(provider: SearchProvider) -> str:
    return getattr(provider, "name", provider.__class__.__name__)


class DuckDuckGoProvider:
    name = "DuckDuckGo"

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, str]]:
        from ..utils.http_client import get_http_client

        client = await get_http_client()
        search_url = "https://api.duckduckgo.com/"
        params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

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
                                    "title": text.split(" - ")[0] if " - " in text else text[:50],
                                    "url": topic["FirstURL"],
                                    "snippet": text,
                                }
                            )

        return results


class BraveSearchProvider:
    name = "Brave Search"

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, str]]:
        from ..utils.http_client import get_http_client

        client = await get_http_client()

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["X-Subscription-Token"] = self.api_key

        search_url = "https://api.search.brave.com/res/v1/web/search"
        params = {"q": query, "count": min(num_results, 20)}

        try:
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


class DuckDuckGoHTMLProvider:
    name = "DuckDuckGo HTML"

    async def search(self, query: str, num_results: int = 5) -> list[dict[str, str]]:
        from ..utils.http_client import get_http_client

        client = await get_http_client()
        search_url = "https://html.duckduckgo.com/html/"
        data = {"q": query, "b": ""}
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        try:
            resp = await client.post(search_url, data=data, headers=headers)

            if resp.status_code != 200:
                logger.warning(f"DuckDuckGo HTML error: status {resp.status_code}")
                return []

            soup = BeautifulSoup(resp.text, "html.parser")
            results = []

            for result in soup.select(".result"):
                if len(results) >= num_results:
                    break

                title_elem = result.select_one(".result__title")
                url_elem = result.select_one(".result__url")
                snippet_elem = result.select_one(".result__snippet")

                if title_elem and url_elem:
                    title = title_elem.get_text(strip=True)
                    url = url_elem.get("href", "")
                    snippet = snippet_elem.get_text(strip=True) if snippet_elem else ""

                    if url.startswith("//"):
                        url = "https:" + url

                    results.append(
                        {
                            "title": title,
                            "url": url,
                            "snippet": snippet,
                        }
                    )

            return results
        except Exception as e:
            logger.warning(f"DuckDuckGo HTML exception: {e}")
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


async def search_with_fallback(query: str, num_results: int = 5) -> list[dict[str, str]]:
    from ..core.config import settings

    providers: list[SearchProvider] = [
        DuckDuckGoProvider(),
        DuckDuckGoHTMLProvider(),
        BraveSearchProvider(
            api_key=settings.brave_api_key if hasattr(settings, "brave_api_key") else None
        ),
    ]

    for provider in providers:
        provider_name = get_provider_name(provider)
        logger.info(f"Trying search provider: {provider_name}")
        results = await provider.search(query, num_results)
        if results:
            logger.info(f"{provider_name} returned {len(results)} results")
            return results
        logger.warning(f"{provider_name} returned no results")

    return []
