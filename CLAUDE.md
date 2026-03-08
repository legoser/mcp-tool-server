# Project: MCP Tools Server (Python)

## Quick Commands

- **Install (Required first)**: `pip install -e .`
- **Run (Stdio/MCP)**: `python -m src`
- **Run (SSE/HTTP)**: `python -m src.main_sse` or `python -m uvicorn src.main_sse:app --host 0.0.0.0 --port 3344`
- **Run (SSE/HTTP, Custom Host/Port)**: `SERVER_HOST=0.0.0.0 SERVER_PORT=3344 python -m src.main_sse`
- **Inspector (FastMCP)**: `fastmcp dev inspector python -m src` ← Use this, NOT `src/main.py`
- **Lint**: `ruff check .`
- **Format**: `ruff format .`
- **Test**: `pytest`

## Tech Stack

- **Framework**: `mcp` (Python SDK)
- **Runtime**: Python 3.10+ (Asyncio)
- **Validation**: Pydantic v2
- **HTTP**: `httpx` (async), `beautifulsoup4` (parsing)
- **SSE Server**: FastAPI + uvicorn

## Project Structure

- `src/main.py` — Stdio entry point
- `src/main_sse.py` — SSE/HTTP entry point (port 3344)
- `src/server.py` — MCP Server configuration
- `src/tools/` — Инструменты с декоратором `@mcp.tool()`
- `src/core/` — Конфигурация и логирование
- `src/utils/` — Вспомогательные функции:
  - `rate_limiter.py` — Rate limiting для HTTP запросов
  - `search_providers.py` — Провайдеры поиска (DuckDuckGo, Brave)
  - `web_fetcher.py` — Загрузка и парсинг веб-страниц
  - `http_client.py` — Общий HTTP клиент

## Available Tools

| Tool | Description |
|------|-------------|
| `get_current_time` | Текущее время (МСК) |
| `get_random_joke` | Случайная шутка |
| `get_random_quote` | Случайная цитата |
| `get_random_fact` | Случайный факт |
| `web_search` | Поиск в интернете (DuckDuckGo HTML) |
| `web_fetch` | Загрузка веб-страницы |
| `generate_text` | Генерация текста (Ollama) |
| `chat_with_ai` | Чат с AI (Ollama) |
| `list_ollama_models` | Список моделей Ollama |

## Configuration

Server configuration is controlled via environment variables (defined in `src/core/config.py`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_HOST` | `0.0.0.0` | Server bind address (0.0.0.0 = accessible from external networks) |
| `SERVER_PORT` | `3344` | Server port |
| `CLIENT_BASE_URL` | `http://0.0.0.0:3344` | Base URL for client connections |

Examples:
- **Custom host/port**: `SERVER_HOST=127.0.0.1 SERVER_PORT=8080 python -m src.main_sse`
- **Listen on all interfaces**: `SERVER_HOST=0.0.0.0 SERVER_PORT=3344 python -m src.main_sse` (default)

## Coding Standards

- **Asyncio**: Все хендлеры ДОЛЖНЫ быть `async def`
- **Type Hints**: Обязательные аннотации типов
- **Docstrings**: Google-style — описание используется для инструментов
- **Logging**: `src.core.logging` — логи в stderr

## Tool Development Rules

- Каждый инструмент — функция с декоратором `@mcp.tool()`
- Имена: `snake_case`
- Ошибки: информативные исключения или текстовое описание
- Зависимости: добавлять в `pyproject.toml`
- **Общая логика** (HTTP, rate limiting, парсинг) — в `src/utils/`
- **Инструменты** — только в `src/tools/`

## Deployment

- **Stdio**: Claude Desktop, MCP Inspector
- **SSE**: `python -m src.main_sse` (uses SERVER_HOST and SERVER_PORT from env or defaults)
