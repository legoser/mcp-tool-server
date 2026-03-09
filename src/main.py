"""Main entry point for MCP server."""

import asyncio

from . import (
    prompts,  # noqa: F401 - needed to register prompts
    tools,  # noqa: F401 - needed to register tools
)
from .core.config import settings
from .core.logging import get_logger
from .mcp import mcp

logger = get_logger(__name__)


async def run_http():
    """Run the MCP server with HTTP transport."""
    await mcp.run_async(
        transport="streamable-http",
        host=settings.HOST,
        port=settings.PORT,
        stateless_http=settings.FASTMCP_STATELESS_HTTP,
    )


def main() -> None:
    """Run the MCP server."""
    if settings.TRANSPORT == "http":
        logger.info(
            f"Starting HTTP server on {settings.HOST}:{settings.PORT}, "
            f"stateless={settings.FASTMCP_STATELESS_HTTP}"
        )
        asyncio.run(run_http())
    else:
        logger.info("Starting stdio server")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
