# Project: MCP Tools Server (Python)

## Quick Commands
- **Install (Required first)**: `pip install -e .`
- **Run (Stdio/MCP)**: `python -m src`
- **Run (SSE/HTTP)**: `python -m uvicorn src.main_sse:app --port 3344`
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
- **SSE**: `uvicorn src.main_sse:app --port 3344`
