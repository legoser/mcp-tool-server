"""Unit tests for all MCP tools with mocked HTTP."""

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


async def test_get_current_time():
    from src.tools.time_tools import get_current_time

    result = await get_current_time()
    assert "МСК" in result
    assert "." in result


async def test_get_random_joke():
    from src.tools.http_tools import get_random_joke

    mock_json = {"setup": "Test joke?", "punchline": "Test punchline!"}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("src.tools.http_tools.get_http_client", return_value=mock_client):
        result = await get_random_joke()
        assert "Test joke?" in result
        assert "Test punchline!" in result


async def test_get_random_quote():
    from src.tools.http_tools import get_random_quote

    mock_json = [{"q": "Test quote", "a": "Author"}]

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("src.tools.http_tools.get_http_client", return_value=mock_client):
        result = await get_random_quote()
        assert "Test quote" in result


async def test_get_random_fact():
    from src.tools.http_tools import get_random_fact

    mock_json = {"text": "Test fact"}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("src.tools.http_tools.get_http_client", return_value=mock_client):
        result = await get_random_fact()
        assert "Test fact" in result


async def test_web_search():
    from src.tools.web_tools import web_search

    mock_results = [
        {
            "title": "Python",
            "url": "https://python.org",
            "snippet": "Python is a programming language",
        },
        {"title": "Example", "url": "https://example.com", "snippet": "Example site"},
    ]

    with patch("src.tools.web_tools.search_with_fallback", return_value=mock_results):
        result = await web_search("python", num_results=3)
        assert "Python" in result
        assert "python.org" in result


async def test_web_fetch():
    from src.tools.web_tools import web_fetch
    from src.utils.web_fetcher import WebFetcher

    mock_fetcher = AsyncMock(spec=WebFetcher)
    mock_fetcher.fetch = AsyncMock(
        return_value="Заголовок: Test\n\nURL: http://example.com\n\nСодержимое:\nTest content"
    )

    with patch("src.tools.web_tools.get_fetcher", return_value=mock_fetcher):
        result = await web_fetch("http://example.com")
        assert "Test" in result


async def test_generate_text():
    from src.tools.ollama_tools import generate_text

    mock_json = {"choices": [{"text": "Generated text"}]}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch("src.tools.ollama_tools.get_http_client", return_value=mock_client):
        result = await generate_text("Hello")
        assert "Generated text" in result


async def test_chat_with_ai():
    from src.tools.ollama_tools import chat_with_ai

    mock_json = {"choices": [{"message": {"content": "AI response"}}]}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.post = AsyncMock(return_value=mock_response)

    with patch("src.tools.ollama_tools.get_http_client", return_value=mock_client):
        result = await chat_with_ai("System", "Hello")
        assert "AI response" in result


async def test_list_ollama_models():
    from src.tools.ollama_tools import list_ollama_models

    mock_json = {"models": [{"name": "llama3"}, {"name": "qwen2.5"}]}

    mock_response = MagicMock()
    mock_response.json = MagicMock(return_value=mock_json)
    mock_response.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.get = AsyncMock(return_value=mock_response)

    with patch("src.tools.ollama_tools.get_http_client", return_value=mock_client):
        result = await list_ollama_models()
        assert "llama3" in result
        assert "qwen2.5" in result


async def run_all_tests():
    print("=" * 50)
    print("Running tool tests...")
    print("=" * 50)

    tests = [
        ("get_current_time", test_get_current_time),
        ("get_random_joke", test_get_random_joke),
        ("get_random_quote", test_get_random_quote),
        ("get_random_fact", test_get_random_fact),
        ("web_search", test_web_search),
        ("web_fetch", test_web_fetch),
        ("generate_text", test_generate_text),
        ("chat_with_ai", test_chat_with_ai),
        ("list_ollama_models", test_list_ollama_models),
    ]

    passed = 0
    failed = 0

    for name, test_func in tests:
        try:
            await test_func()
            print(f"✓ {name}")
            passed += 1
        except Exception as e:
            print(f"✗ {name}: {e}")
            failed += 1

    print("=" * 50)
    print(f"Passed: {passed}/{passed + failed}")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(run_all_tests())
