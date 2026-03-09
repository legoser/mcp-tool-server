"""Main entry point for MCP server."""

import asyncio
import os

from . import (
    prompts,  # noqa: F401 - needed to register prompts
    tools,  # noqa: F401 - needed to register tools
)
from .core.logging import get_logger, setup_logging
from .mcp import mcp

setup_logging()
logger = get_logger(__name__)

HOST = os.getenv("SERVER_HOST", "0.0.0.0")
PORT = int(os.getenv("SERVER_PORT", "3344"))
TRANSPORT = os.getenv("TRANSPORT", "http")
STATELESS = os.getenv("FASTMCP_STATELESS_HTTP", "true").lower() == "true"


async def run_http():
    """Run the MCP server with HTTP transport."""
    await mcp.run_async(
        transport="streamable-http",
        host=HOST,
        port=PORT,
        stateless_http=STATELESS,
    )


def main() -> None:
    """Run the MCP server."""
    if TRANSPORT == "http":
        logger.info(f"Starting HTTP server on {HOST}:{PORT}, stateless={STATELESS}")
        asyncio.run(run_http())
    else:
        logger.info("Starting stdio server")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
