"""FastAPI SSE server for MCP."""

import json
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

# Handle both: relative imports and direct execution
try:
    from .core.config import settings
    from .core.logging import get_logger, setup_logging
    from .server import get_server
except ImportError:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
    from src.core.config import settings
    from src.core.logging import get_logger, setup_logging
    from src.server import get_server

logger = get_logger(__name__)
setup_logging()

# Session management
_sessions: dict[str, dict] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context for FastAPI app."""
    logger.info("App startup")
    yield
    logger.info("App shutdown")


app = FastAPI(
    title="MCP Tools Server SSE",
    description="MCP server with SSE transport",
    lifespan=lifespan,
)


@app.get("/sse")
async def sse_endpoint(request: Request) -> EventSourceResponse:
    """SSE connection endpoint for MCP protocol."""
    import uuid

    session_id = str(uuid.uuid4())
    _sessions[session_id] = {
        "id": session_id,
        "messages": [],
        "closed": False,
    }
    logger.info(f"SSE session created: {session_id}")

    async def event_generator() -> AsyncGenerator[str, None]:
        """Generate SSE events."""
        try:
            # Send initial session message with session_id
            init_msg = {
                "jsonrpc": "2.0",
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {},
                    "serverInfo": {
                        "name": "MCP Tools Server",
                        "version": "0.1.0",
                    },
                    "sessionId": session_id,
                },
            }
            yield f"data: {json.dumps(init_msg, ensure_ascii=False)}\n\n"

            # Keep connection alive
            import asyncio

            while not _sessions[session_id]["closed"]:
                # Check for messages to send
                messages = _sessions[session_id]["messages"]
                if messages:
                    msg = messages.pop(0)
                    yield f"data: {json.dumps(msg, ensure_ascii=False)}\n\n"

                await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"SSE error: {e}")
            yield f"data: {json.dumps({'error': str(e)}, ensure_ascii=False)}\n\n"
        finally:
            _sessions[session_id]["closed"] = True
            logger.info(f"SSE session closed: {session_id}")

    return EventSourceResponse(event_generator())


@app.post("/message")
async def message_endpoint(request: Request) -> JSONResponse:
    """Handle MCP messages (JSONRPC)."""
    session_id = request.query_params.get("session_id")

    if not session_id or session_id not in _sessions:
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32600,
                    "message": "Invalid session",
                },
            },
        )

    try:
        body = await request.json()
        logger.debug(f"Received message: {body}")

        # Handle JSONRPC 2.0 protocol
        if not isinstance(body, dict) or "jsonrpc" not in body:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request",
                    },
                },
            )

        request_id = body.get("id")
        method = body.get("method")
        params = body.get("params", {})

        # Log the method call
        logger.info(f"[{session_id}] Method: {method}, Params: {params}")

        # Get the server and handle the request
        server = get_server()

        if method == "tools/list":
            tools_list = await server.list_tools()
            tools = []
            for tool in tools_list:
                tools.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "inputSchema": tool.inputSchema or {},
                })

            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools,
                },
            }
        elif method == "tools/call":
            # Handle tool calls
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            # Find the tool and call it
            response = await _call_tool(server, tool_name, tool_args, request_id)

        else:
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            }

        # Queue message to be sent via SSE
        if session_id in _sessions:
            _sessions[session_id]["messages"].append(response)

        return JSONResponse({"status": "ok", "queued": True})

    except Exception as e:
        logger.error(f"Message handling error: {e}", exc_info=True)
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}",
                },
            },
        )


@app.post("/mcp")
async def mcp_endpoint(request: Request) -> JSONResponse:
    """
    Standard MCP HTTP endpoint (JSON-RPC 2.0).
    Compatible with LM Studio, Cursor, Claude Desktop, and other MCP clients.
    This is the primary endpoint for standard MCP protocol.
    """
    try:
        body = await request.json()
        logger.debug(f"MCP request: {body}")

        # Validate JSON-RPC 2.0 structure
        if not isinstance(body, dict) or "jsonrpc" not in body:
            return JSONResponse(
                {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request",
                    },
                },
                status_code=400,
            )

        request_id = body.get("id")
        method = body.get("method")
        params = body.get("params", {})

        logger.info(f"MCP method: {method}, ID: {request_id}")

        # Get the server instance
        server = get_server()

        # Handle MCP protocol methods
        if method == "initialize":
            # Client initialization
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {},
                    },
                    "serverInfo": {
                        "name": "MCP Tools Server",
                        "version": "0.1.0",
                    },
                },
            }

        elif method == "tools/list":
            # List all available tools
            tools_list = await server.list_tools()
            tools = []
            for tool in tools_list:
                tools.append({
                    "name": tool.name,
                    "description": tool.description or "",
                    "inputSchema": tool.inputSchema or {},
                })

            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": {
                    "tools": tools,
                },
            }

        elif method == "tools/call":
            # Call a specific tool
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})

            try:
                logger.info(f"Calling tool '{tool_name}' with args: {tool_args}")
                result = await server.call_tool(tool_name, tool_args)

                logger.info(f"Tool result type: {type(result)}, value: {result}")

                # Extract text from result
                # FastMCP returns either (content_blocks, metadata) or just content_blocks
                result_text = ""
                content_blocks = result

                # If result is a tuple, unpack it
                if isinstance(result, tuple):
                    if len(result) >= 1:
                        content_blocks = result[0]
                    logger.info(f"Unpacked tuple, content_blocks type: {type(content_blocks)}")

                # Extract text from content blocks
                if isinstance(content_blocks, list) and content_blocks:
                    # It's a list of ContentBlock objects
                    for block in content_blocks:
                        logger.info(f"Block type: {type(block)}, has text: {hasattr(block, 'text')}")
                        if hasattr(block, 'text'):
                            result_text = block.text
                            logger.info(f"Extracted text from block: {result_text[:100] if result_text else '(empty)'}")
                            break
                        elif isinstance(block, dict) and 'text' in block:
                            result_text = block['text']
                            logger.info(f"Extracted text from dict block: {result_text[:100] if result_text else '(empty)'}")
                            break

                    if not result_text and len(content_blocks) > 0:
                        # Fallback: convert first item to string
                        logger.info("No text found in blocks, using str()")
                        result_text = str(content_blocks[0])
                else:
                    result_text = str(content_blocks) if content_blocks is not None else ""

                logger.info(f"Final result_text: {result_text[:100] if result_text else '(empty)'}")

                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result_text,
                            }
                        ],
                        "isError": False,
                    },
                }
            except Exception as e:
                logger.error(f"Tool call error for '{tool_name}': {e}", exc_info=True)
                response = {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32603,
                        "message": f"Tool error: {str(e)}",
                    },
                }

        else:
            # Method not implemented
            response = {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}",
                },
            }

        # Ensure response is JSON serializable
        try:
            response_json = json.dumps(response, ensure_ascii=False)
            logger.info(f"MCP response JSON length: {len(response_json)} bytes")
            logger.info(f"MCP response preview: {response_json[:300]}")
        except Exception as e:
            logger.error(f"Failed to serialize response: {e}")
            response_json = "{}"
        return JSONResponse(response)

    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in request: {e}")
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {str(e)}",
                },
            },
            status_code=400,
        )
    except Exception as e:
        logger.error(f"MCP endpoint error: {e}", exc_info=True)
        return JSONResponse(
            {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal server error: {str(e)}",
                },
            },
            status_code=500,
        )


async def _call_tool(server, tool_name: str, tool_args: dict, request_id: int) -> dict:
    """Call a tool and return the response."""
    try:
        logger.info(f"Calling tool '{tool_name}' with args: {tool_args}")

        # Use FastMCP's built-in call_tool method
        result = await server.call_tool(tool_name, tool_args)

        logger.info(f"Tool result type: {type(result)}, value: {result}")

        # result is a list of ContentBlock objects, extract text
        # FastMCP returns either (content_blocks, metadata) or just content_blocks
        result_text = ""
        content_blocks = result

        # If result is a tuple, unpack it
        if isinstance(result, tuple):
            if len(result) >= 1:
                content_blocks = result[0]
            logger.info(f"Unpacked tuple, content_blocks type: {type(content_blocks)}")

        # Extract text from content blocks
        if isinstance(content_blocks, list) and content_blocks:
            # It's a list of ContentBlock
            for block in content_blocks:
                logger.info(f"Block type: {type(block)}, has text: {hasattr(block, 'text')}")
                if hasattr(block, 'text'):
                    result_text = block.text
                    logger.info(f"Extracted text from block: {result_text[:100] if result_text else '(empty)'}")
                    break
                elif isinstance(block, dict) and 'text' in block:
                    result_text = block['text']
                    logger.info(f"Extracted text from dict block: {result_text[:100] if result_text else '(empty)'}")
                    break

            if not result_text and len(content_blocks) > 0:
                # Fallback: convert first item to string
                logger.info("No text found in blocks, using str()")
                result_text = str(content_blocks[0])
        else:
            result_text = str(content_blocks) if content_blocks is not None else ""

        logger.info(f"Final result_text: {result_text[:100] if result_text else '(empty)'}")

        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result_text,
                    }
                ],
                "isError": False,
            },
        }

    except Exception as e:
        logger.error(f"Tool error for '{tool_name}': {e}", exc_info=True)
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": -32603,
                "message": f"Internal error: {str(e)}",
            },
        }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return JSONResponse({"status": "ok"})


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Starting SSE server on {settings.server_host}:{settings.server_port}")
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level="info",
    )
