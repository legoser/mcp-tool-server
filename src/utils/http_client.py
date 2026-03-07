import httpx

_default_client: httpx.AsyncClient | None = None
_ssl_client: httpx.AsyncClient | None = None


async def get_http_client(verify: bool = False) -> httpx.AsyncClient:
    global _default_client, _ssl_client

    if verify:
        if _ssl_client is None:
            _ssl_client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                follow_redirects=True,
                trust_env=True,
            )
        return _ssl_client
    else:
        if _default_client is None:
            _default_client = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                follow_redirects=True,
            )
        return _default_client


async def close_http_client() -> None:
    global _default_client, _ssl_client
    if _default_client is not None:
        await _default_client.aclose()
        _default_client = None
    if _ssl_client is not None:
        await _ssl_client.aclose()
        _ssl_client = None
