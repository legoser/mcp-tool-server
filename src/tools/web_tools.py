from ..utils.search_providers import search_with_fallback
from ..utils.web_fetcher import get_fetcher


async def web_search(query: str, num_results: int = 5) -> str:
    """Выполняет поиск в интернете и возвращает список релевантных результатов.

    Пробует провайдеры по очереди: DuckDuckGo API → DuckDuckGo HTML → Brave Search.

    Args:
        query: Поисковый запрос
        num_results: Количество результатов (по умолчанию 5)
    """
    results = await search_with_fallback(query, num_results)

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
    fetcher = await get_fetcher()
    return await fetcher.fetch(url)
