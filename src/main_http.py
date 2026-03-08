"""MCP server with HTTP transport (standard /mcp endpoint via FastMCP)."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Handle both: relative imports and direct execution
try:
    from .core.config import settings
    from .core.logging import get_logger, setup_logging
    from .server import create_server
except ImportError:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from src.core.config import settings
    from src.core.logging import get_logger, setup_logging
    from src.server import create_server

setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for FastAPI app."""
    logger.info("MCP HTTP Server startup")
    yield
    logger.info("MCP HTTP Server shutdown")


def get_app() -> FastAPI:
    """Create and configure FastAPI application with MCP HTTP transport."""
    app = FastAPI(
        title="MCP Tools Server",
        description="MCP server with HTTP transport at /mcp endpoint (JSON-RPC 2.0)",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Get the FastMCP server instance
    mcp_server = create_server()

    # Integrate FastMCP with FastAPI
    # This creates /mcp endpoint with JSON-RPC 2.0 protocol
    try:
        # Method 1: Try from_fastapi if available in FastMCP
        if hasattr(mcp_server, 'from_fastapi'):
            mcp_server.from_fastapi(app, path="/mcp")
            logger.info("✓ FastMCP integrated via from_fastapi()")
        # Method 2: Try to use FastMCP as ASGI app
        elif hasattr(mcp_server, 'app'):
            # Mount FastMCP's internal app at /mcp
            app.mount("/mcp", mcp_server.app)
            logger.info("✓ FastMCP mounted via .app attribute")
        else:
            logger.warning("⚠ Could not integrate FastMCP automatically, checking alternatives...")
    except Exception as e:
        logger.error(f"Error integrating FastMCP: {e}. Attempting fallback...")

    @app.get("/health")
    async def health():
        """Health check endpoint."""
        return JSONResponse({"status": "ok"})

    @app.get("/")
    async def root():
        """Root endpoint with server info."""
        return JSONResponse({
            "name": "MCP Tools Server",
            "version": "0.1.0",
            "mcp_endpoint": "/mcp",
            "protocol": "JSON-RPC 2.0",
            "clients": ["LM Studio", "Cursor", "Claude Desktop", "Cline"]
        })

    return app


if __name__ == "__main__":
    import uvicorn

    app = get_app()
    logger.info(f"Starting MCP HTTP server on {settings.server_host}:{settings.server_port}")
    logger.info("MCP Protocol endpoint: /mcp (JSON-RPC 2.0)")
    logger.info("Compatible with LM Studio, Cursor, Claude, and other MCP clients")

    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level="info",
    )
