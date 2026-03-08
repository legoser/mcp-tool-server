"""Main entry point for MCP server."""

import asyncio
import sys
from pathlib import Path

# Handle both: relative imports (when loaded as module) and direct execution
try:
    from .server import create_server
    from .core.logging import get_logger, setup_logging
except ImportError:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from src.server import create_server
    from src.core.logging import get_logger, setup_logging

logger = get_logger(__name__)
setup_logging()


class ServerWrapper:
    """Wrapper to provide server_main compatibility."""
    
    def run(self, transport: str = "stdio"):
        """Run the server with specified transport."""
        logger.info(f"Starting MCP server with transport: {transport}")
        server = create_server()
        server.run(transport=transport)


# Export server_main for compatibility with pyproject.toml and other imports
server_main = ServerWrapper()


if __name__ == "__main__":
    server_main.run(transport="stdio")
