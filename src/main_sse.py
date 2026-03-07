from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from mcp.server import Server
from mcp.server.sse import SseServerTransport
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


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    setup_logging()
    logger.info("Starting MCP Tools Server (SSE)")
    yield
    logger.info("Shutting down MCP Tools Server")


app = FastAPI(title="MCP Tools Server", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

mcp_server = create_server()
sse_transport = SseServerTransport("/messages/")


@app.get("/sse")
async def sse_handler(request: Request):
    try:
        async with sse_transport.connect_sse(
            request.scope, request.receive, request._send
        ) as streams:
            await mcp_server.run(
                streams[0],
                streams[1],
                mcp_server.create_initialization_options(),
            )
    except Exception:
        pass
    return Response(status_code=200, media_type="text/event-stream")


@app.post("/messages/")
async def messages_handler(request: Request):
    try:
        await sse_transport.handle_post_message(request.scope, request.receive, request._send)
    except Exception as e:
        logger.error(f"Message handler error: {e}")
        return Response(content="Internal server error", status_code=500)


@app.get("/")
async def root():
    return {
        "name": "MCP Tools Server",
        "version": "0.1.0",
        "endpoints": {
            "sse": "/sse",
            "messages": "/messages/",
        },
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3344)
