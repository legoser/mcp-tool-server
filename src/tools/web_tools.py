from bs4 import BeautifulSoup

from src.core.logging import get_logger
from src.utils.http_client import get_http_client

logger = get_logger(__name__)


async def web_search(query: str, num_results: int = 5) -> str:
    """Выполняет поиск в интернете и возвращает список релевантных результатов.

    Args:
        query: Поисковый запрос
        num_results: Количество результатов (по умолчанию 5)
    """
    client = await get_http_client()

    search_url = "https://api.duckduckgo.com/"
    params = {"q": query, "format": "json", "no_html": "1", "skip_disambig": "1"}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    resp = await client.get(search_url, params=params, headers=headers)

    if resp.status_code not in (200, 202):
        return f"Ошибка поиска: статус {resp.status_code}"

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

    if not results:
        return "Результаты не найдены"

    output = f'Результаты поиска по запросу "{query}":\n\n'
    for i, r in enumerate(results[:num_results], 1):
        output += f"{i}. {r['title']}\n"
        output += f"   URL: {r['url']}\n"
        if r["snippet"]:
            output += f"   {r['snippet']}\n"
        output += "\n"

    return output


async def web_fetch(url: str) -> str:
    """Загружает и возвращает содержимое веб-страницы.

    Args:
        url: URL адрес страницы для загрузки
    """
    client = await get_http_client(verify=True)

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

    try:
        resp = await client.get(url, headers=headers, follow_redirects=True)
    except Exception as e:
        return f"Ошибка при загрузке: {str(e)}"

    content_type = resp.headers.get("content-type", "")

    if "text/html" in content_type:
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()

        title = soup.title.string if soup.title else "Без заголовка"

        text = soup.get_text(separator="\n", strip=True)

        max_length = 8000
        if len(text) > max_length:
            text = text[:max_length] + "\n\n... (текст обрезан)"

        return f"Заголовок: {title}\n\nURL: {url}\n\nСодержимое:\n{text}"

    return f"URL: {url}\n\nТип контента: {content_type}\n\n{resp.text[:5000]}"
