# MCP Tools Server

FastMCP server (Python 3.10+, asyncio). Tools in `src/tools/`, prompts in `src/prompts/`.

## Commands
- `pip install -e .` — install
- `python -m src` — run stdio
- `TRANSPORT=http python -m src` — run HTTP (port 3344)
- `pytest` / `ruff check src/` / `ruff format src/`

## Standards
- All handlers: `async def` with type hints
- Docstrings: Google-style (used as tool/prompt description)
- Logging: `from src.core.logging import get_logger`
- New tools: `@mcp.tool()` in `src/tools/`, add deps to `pyproject.toml`
