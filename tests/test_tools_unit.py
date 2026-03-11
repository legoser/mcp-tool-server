"""Unit tests for MCP tools."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch


class TestTimeTools:
    @pytest.mark.asyncio
    async def test_get_current_time(self):
        from src.tools.time_tools import get_current_time

        result = await get_current_time()
        assert "МСК" in result
        assert "." in result


class TestHttpTools:
    @pytest.mark.asyncio
    async def test_get_random_joke(self):
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

    @pytest.mark.asyncio
    async def test_get_random_quote(self):
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

    @pytest.mark.asyncio
    async def test_get_random_fact(self):
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


class TestWebTools:
    @pytest.mark.asyncio
    async def test_web_search(self):
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

    @pytest.mark.asyncio
    async def test_web_fetch(self):
        from src.tools.web_tools import web_fetch
        from src.utils.web_fetcher import WebFetcher

        mock_fetcher = AsyncMock(spec=WebFetcher)
        mock_fetcher.fetch = AsyncMock(
            return_value="Заголовок: Test\n\nURL: http://example.com\n\nСодержимое:\nTest content"
        )

        with patch("src.tools.web_tools.get_fetcher", return_value=mock_fetcher):
            result = await web_fetch("http://example.com")
            assert "Test" in result

    @pytest.mark.asyncio
    async def test_web_search_no_results(self):
        from src.tools.web_tools import web_search

        with patch("src.tools.web_tools.search_with_fallback", return_value=[]):
            result = await web_search("nonexistentquery12345")
            assert "не найдены" in result.lower()
