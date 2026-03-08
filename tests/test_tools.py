from unittest.mock import AsyncMock, patch

import pytest

from src.tools.http_tools import get_random_fact, get_random_joke, get_random_quote
from src.tools.time import get_current_time


class TestTimeTools:
    @pytest.mark.asyncio
    async def test_get_current_time(self):
        result = get_current_time()
        assert "МСК" in result
        assert "." in result


class TestHttpTools:
    @pytest.mark.asyncio
    @patch("src.tools.http_tools.get_http_client")
    async def test_get_random_joke(self, mock_get_client):
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            "setup": "Why did the chicken?",
            "punchline": "To get to the other side!",
        }
        mock_response.raise_for_status = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        result = await get_random_joke()
        assert "Why did the chicken?" in result

    @pytest.mark.asyncio
    @patch("src.tools.http_tools.get_http_client")
    async def test_get_random_quote(self, mock_get_client):
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = [{"q": "Test quote", "a": "Author"}]
        mock_response.raise_for_status = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        result = await get_random_quote()
        assert "Test quote" in result

    @pytest.mark.asyncio
    @patch("src.tools.http_tools.get_http_client")
    async def test_get_random_fact(self, mock_get_client):
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.json.return_value = {"text": "Test fact"}
        mock_response.raise_for_status = AsyncMock()
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        result = await get_random_fact()
        assert "Test fact" in result
