from __future__ import annotations

import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Handle both: relative imports and direct execution
try:
    from .core.logging import get_logger, setup_logging
    from .tools.registry import get_all_tools
except ImportError:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from src.core.logging import get_logger, setup_logging
    from src.tools.registry import get_all_tools

logger = get_logger(__name__)
instructions_text = """
You are a server that provides access to a set of tools.
You will receive requests from clients in the form of JSON objects.
Each request will have the following format:
{
    "tool": "tool_name",
    "args": {
        "arg1": "value1",
        "arg2": "value2",
        ...
    }
}
You should execute the requested tool with the provided arguments
and return the result as a JSON object.
The response should have the following format:
{
    "result": "result_value"
}
If the tool execution fails, you should return an error message in the following format:
{
    "error": "error_message"
}
"""


def create_server() -> FastMCP:
    """Factory function to create FastMCP server instance."""
    return FastMCP(
        name="MCP Tools Server",
        instructions=instructions_text,
        tools=get_all_tools(),
        warn_on_duplicate_tools=True,
        debug=True,
    )


# Module-level cache for lazy loading
_server_instance: FastMCP | None = None


def get_server() -> FastMCP:
    """Get or create the server instance (lazy loading)."""
    global _server_instance
    if _server_instance is None:
        _server_instance = create_server()
    return _server_instance


# Export server_main for compatibility with pyproject.toml
server_main = None  # Will be set by main.py


def init_server_main():
    """Initialize server_main variable."""
    global server_main
    if server_main is None:
        from .main import ServerWrapper
        server_main = ServerWrapper()
