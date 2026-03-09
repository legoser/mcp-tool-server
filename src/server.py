from . import (
    prompts,  # noqa: F401 - needed to register prompts
    tools,  # noqa: F401 - needed to register tools
)
from .core.config import settings
from .core.logging import get_logger
from .mcp import mcp

logger = get_logger(__name__)

__all__ = ["mcp", "settings"]
