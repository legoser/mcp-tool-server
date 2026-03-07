# Project: MCP Tools Server (Python)

## Quick Commands
- **Install**: `pip install -e .`
- **Run (Stdio)**: `python -m src.main`
- **Run (SSE)**: `uvicorn src.main_sse:app --port 3344`
- **Inspector**: `npx @modelcontextprotocol/inspector python -m src.main`
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
- `src/utils/` — Вспомогательные функции

## Available Tools
| Tool | Description |
|------|-------------|
| `get_current_time` | Текущее время (МСК) |
| `get_random_joke` | Случайная шутка |
| `get_random_quote` | Случайная цитата |
| `get_random_fact` | Случайный факт |
| `web_search` | Поиск в интернете |
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

## Deployment
- **Stdio**: Claude Desktop, MCP Inspector
- **SSE**: `uvicorn src.main_sse:app --port 3344`
