# MCP Tools Server (Python)

## Quick Commands

- **Install (Required first)**: `pip install -e .`
- **Run (Stdio)**: `python -m src`
- **Run (HTTP)**: `TRANSPORT=http python -m src`
- **Run (HTTP, custom port)**: `TRANSPORT=http SERVER_PORT=8080 python -m src`
- **Inspector**: `fastmcp dev inspector python -m src`
- **Lint**: `ruff check src/`
- **Format**: `ruff format src/`
- **Test (unit)**: `pytest tests/test_tools_unit.py -v`

## Running Tests

**Unit tests** (tests tools directly without starting server):

```bash
pytest tests/test_tools_unit.py -v
```

Tests use mocked HTTP clients and don't require a running MCP server.

## Tech Stack

- **Framework**: `fastmcp` (Streamable HTTP transport)
- **Runtime**: Python 3.10+ (Asyncio)
- **Validation**: Pydantic v2
- **HTTP**: `httpx` (async), `beautifulsoup4` (parsing)
- **Logging**: `structlog` (structured logging)

## Project Structure

```shell
src/
├── __init__.py         # Package init
├── __main__.py        # Entry point for python -m src
├── main.py            # Main server logic
├── mcp.py             # FastMCP server definition
├── server.py         # Server exports and config
├── core/
│   ├── config.py      # Configuration settings
│   └── logging.py    # Structured logging (structlog)
├── prompts/          # @mcp.prompt() decorators
│   ├── __init__.py
│   ├── code_review.py
│   ├── debugging.py
│   ├── code_generator.py
│   ├── test_generator.py
│   ├── refactoring.py
│   ├── code_explainer.py
│   ├── documentation.py
│   ├── security_audit.py
│   ├── performance.py
│   ├── sql_query.py
│   ├── api_design.py
│   └── architecture.py
├── tools/            # @mcp.tool() decorators
│   ├── __init__.py
│   ├── time_tools.py
│   ├── http_tools.py
│   ├── web_tools.py
│   ├── weather_tools.py
└── utils/            # Helper functions
    ├── http_client.py
    ├── rate_limiter.py
    ├── search_providers.py
    └── web_fetcher.py
```

## Available Tools

| Tool | Description |
|------|-------------|
| `get_current_time` | Текущее время (МСК) |
| `get_random_joke` | Случайная шутка |
| `get_random_quote` | Случайная цитата |
| `get_random_fact` | Случайный факт |
| `web_search` | Поиск в интернете (DuckDuckGo HTML) |
| `web_fetch` | Загрузка веб-страниц |

## Available Prompts

| Prompt | Description |
|--------|-------------|
| `review_code` | Code Review Agent |
| `debug_error` | Debug Assistant Agent |
| `generate_code` | Code Generator Agent |
| `generate_tests` | Test Generator Agent |
| `refactor_code` | Refactoring Agent |
| `explain_code` | Code Explainer Agent |
| `generate_docs` | Documentation Agent |
| `security_audit` | Security Audit Agent |
| `optimize_performance` | Performance Optimizer Agent |
| `generate_sql` | SQL Query Agent |
| `design_api` | API Design Agent |
| `architecture_advice` | Architecture Advisor Agent |

## MCP Endpoint

The server exposes the standard MCP protocol at `/mcp`.

**Example: List all tools**

```bash
curl -X POST http://localhost:3344/mcp \n  -H "Content-Type: application/json" \n  -H "Accept: application/json, text/event-stream" \n  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'\n```

**Example: Call a tool**

```bash
curl -X POST http://localhost:3344/mcp \n  -H "Content-Type: application/json" \n  -H "Accept: application/json, text/event-stream" \n  -d '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"get_current_time","arguments":{}}}'\n```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_HOST` | `0.0.0.0` | Server bind address |
| `SERVER_PORT` | `3344` | Server port |
| `TRANSPORT` | `stdio` | Transport: `stdio` or `http` |
| `FASTMCP_STATELESS_HTTP` | `true` | Stateless mode for HTTP |
| `LOG_LEVEL` | `INFO` | Log level (DEBUG, INFO, WARNING, ERROR) |
| `LOG_FORMAT` | `console` | Log format: `console` or `json` |

## Logging

The server uses `structlog` for structured logging:

- **Console format** (default): Human-readable with colors
- **JSON format**: Set `LOG_FORMAT=json` for machine-readable output

Example:
```bash
LOG_FORMAT=json LOG_LEVEL=DEBUG TRANSPORT=http python -m src
```

## Coding Standards

- **Asyncio**: All handlers must be `async def`
- **Type Hints**: Required annotations
- **Docstrings**: Google-style — description is used for tools/prompts
- **Logging**: Use `src.core.logging` for structured logging

## Tool/Prompt Development

- Tools: Functions with `@mcp.tool()` decorator in `src/tools/`
- Prompts: Functions with `@mcp.prompt()` decorator in `src/prompts/`
- Names: `snake_case`
- Errors: Informative exceptions or text description
- Dependencies: Add to `pyproject.toml`
