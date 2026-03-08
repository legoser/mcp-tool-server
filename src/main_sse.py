"""FastAPI SSE server for MCP."""

import json
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncGenerator

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

# Handle both: relative imports and direct execution
try:
    from .core.logging import get_logger, setup_logging
    from .server import get_server
except ImportError:
    project_root = Path(__file__).parent.parent
    sys.path.insert(0, str(project_root))
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


async def _call_tool(server, tool_name: str, tool_args: dict, request_id: int) -> dict:
    """Call a tool and return the response."""
    try:
        logger.debug(f"Calling tool {tool_name} with args: {tool_args}")
        
        # Use FastMCP's built-in call_tool method
        result = await server.call_tool(tool_name, tool_args)
        
        # result is a list of ContentBlock objects, extract text
        result_text = ""
        if isinstance(result, list) and result:
            # It's a list of ContentBlock
            for block in result:
                if hasattr(block, 'text'):
                    result_text = block.text
                    break
        else:
            result_text = str(result)
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": result_text,
                    }
                ]
            },
        }
        
    except Exception as e:
        logger.error(f"Tool error: {e}", exc_info=True)
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
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=3344,
        log_level="info",
    )
