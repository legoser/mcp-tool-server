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
STATELESS = os.getenv("FASTMCP_STATELESS_HTTP", "true").lower() == "true"

__all__ = ["mcp", "HOST", "PORT", "STATELESS"]
