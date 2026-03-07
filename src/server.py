from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from src.core.logging import get_logger, setup_logging
from src.tools.registry import get_all_tools

logger = get_logger(__name__)


def create_server() -> Server:
    server = Server("mcp-tools-server")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        logger.info("Listing tools")
        tools = []
        for tool_func in get_all_tools():
            tools.append(
                Tool(
                    name=tool_func.__name__,
                    description=tool_func.__doc__ or "",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                    },
                )
            )
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None = None) -> list[TextContent]:
        logger.info(f"Calling tool: {name} with args: {arguments}")

        for tool_func in get_all_tools():
            if tool_func.__name__ == name:
                result = await tool_func(**(arguments or {}))
                return [TextContent(type="text", text=str(result))]

        raise ValueError(f"Tool not found: {name}")

    return server


async def main():
    setup_logging()
    logger.info("Starting MCP Tools Server (stdio)")

    server = create_server()

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )
