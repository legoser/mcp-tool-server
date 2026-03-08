import sys
from pathlib import Path
from mcp.server.fastmcp.tools import Tool

# Handle both: relative imports and direct execution
try:
    from . import http_tools, ollama_tools, time_tools, web_tools, weather_tools
except ImportError:
    project_root = Path(__file__).parent.parent.parent
    sys.path.insert(0, str(project_root))
    from src.tools import http_tools, ollama_tools, time_tools, web_tools, weather_tools


def get_all_tools() -> list[Tool]:
    """Return a list of FastMCP `Tool` instances created from local functions."""
    funcs = [
        time_tools.get_current_time,
        http_tools.get_random_joke,
        http_tools.get_random_quote,
        http_tools.get_random_fact,
        web_tools.web_search,
        web_tools.web_fetch,
        weather_tools.get_weather,
        ollama_tools.generate_text,
        ollama_tools.chat_with_ai,
        ollama_tools.list_ollama_models,
    ]

    return [Tool.from_function(f) for f in funcs]
