# Project: MCP Tools Server (Python)

## Quick Commands
- **Install**: `pip install -e .`
- **Run (Stdio)**: `python -m src.main`
- **Inspector**: `npx @modelcontextprotocol/inspector python -m src.main`
- **Lint**: `ruff check .`
- **Format**: `ruff format .`
- **Test**: `pytest`

## Tech Stack
- **Framework**: `mcp` (Python SDK)
- **Runtime**: Python 3.10+ (Asyncio)
- **Validation**: Pydantic v2
- **Tools**: `httpx` (для HTTP-запросов), `beautifulsoup4` (парсинг)

## Project Structure
- `src/main.py` — регистрация сервера и объединение всех инструментов.
- `src/tools/` — отдельные модули с логикой инструментов.
- `src/utils/` — вспомогательные асинхронные функции.

## Coding Standards
- **Asyncio**: Все хендлеры инструментов ДОЛЖНЫ быть `async def`.
- **Type Hints**: Обязательное использование аннотаций типов для всех аргументов функций.
- **Docstrings**: Используй Google-style или ReST docstrings. Claude берет описания инструментов прямо из docstrings функций.
- **Logging**: Используй стандартный `logging` в `stderr`. Никогда не используй `print()`, так как он ломает протокол stdio.

## Tool Development Rules
- Каждый инструмент — это функция с декоратором `@mcp.tool()`.
- Имена инструментов: `snake_case`.
- Ошибки: При сбоях выбрасывай информативные исключения или возвращай описание ошибки в тексте, чтобы LLM поняла, что пошло не так.
- Зависимости: Если инструменту нужны сторонние библиотеки, добавь их в `pyproject.toml` или `requirements.txt`.

## Deployment & Debugging
- Основной способ отладки — `MCP Inspector`.
- Если инструмент требует API-ключей, читай их через `pydantic-settings` или `os.getenv`.
