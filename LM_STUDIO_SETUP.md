# LM Studio Integration Guide

## Overview

The MCP Tools Server now supports **standard MCP HTTP protocol** at the `/mcp` endpoint, fully compatible with LM Studio 0.3.17+ and the Model Context Protocol specification.

## Connection Details

| Parameter | Value |
|-----------|-------|
| **Protocol** | JSON-RPC 2.0 over HTTP |
| **Endpoint** | `/mcp` |
| **Full URL** | `http://your-host:3344/mcp` |
| **Specification** | [modelcontextprotocol.io/spec](https://modelcontextprotocol.io/spec) |

## Setup for LM Studio

### Step 1: Ensure Server is Running

```bash
# Option A: SSE/HTTP Server (with standard /mcp endpoint)
python -m uvicorn src.main_sse:app --port 3344

# Option B: Direct HTTP Server
python -m src.main_http
```

Both options now expose the `/mcp` endpoint with standard MCP protocol.

### Step 2: Create or Update `mcp.json`

Navigate to your LM Studio configuration folder and create/update `mcp.json`:

**Location:**

- **Windows**: `%APPDATA%/LMStudio/mcp.json`
- **macOS**: `~/Library/Application Support/LMStudio/mcp.json`
- **Linux**: `~/.config/LMStudio/mcp.json`

**Content:**

```json
{
  "mcpServers": {
    "mcp-tools-server": {
      "url": "http://localhost:3344/mcp",
      "type": "http",
      "capabilities": {
        "tools": true
      }
    }
  }
}
```

### Step 3: Configure for Remote Access (if needed)

If your MCP server is on a different machine:

```json
{
  "mcpServers": {
    "mcp-tools-server": {
      "url": "http://your-server-ip:3344/mcp",
      "type": "http",
      "capabilities": {
        "tools": true
      }
    }
  }
}
```

### Step 4: Verify Connection

1. **Restart LM Studio**
2. **Check LM Studio Settings** → Under "Model Context Protocol (MCP)" section, you should see:
   - ✅ `mcp-tools-server` listed
   - ✅ Status showing "Connected"
3. **Test Tools** → In chat, the model should be able to access all available tools

## Available Tools

Once connected, the following tools are automatically discovered and available:

| Tool | Description |
|------|-------------|
| `get_current_time` | Get current time (MSK timezone) |
| `get_random_joke` | Fetch random joke |
| `get_random_quote` | Fetch random quote |
| `get_random_fact` | Fetch random interesting fact |
| `web_search` | Search the web (DuckDuckGo) |
| `web_fetch` | Fetch and parse web pages |
| `get_weather` | Get weather data |
| `generate_text` | Generate text using Ollama |
| `chat_with_ai` | Chat with AI using Ollama |
| `list_ollama_models` | List available Ollama models |

## Testing the Connection

### Test 1: Initialize Request

```bash
curl -X POST http://localhost:3344/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {}
  }'
```

Expected response:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2024-11-05",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "MCP Tools Server",
      "version": "0.1.0"
    }
  }
}
```

### Test 2: List Tools

```bash
curl -X POST http://localhost:3344/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```

### Test 3: Call a Tool

```bash
curl -X POST http://localhost:3344/mcp \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "get_current_time",
      "arguments": {}
    }
  }'
```

## URI Endpoints Reference

| Endpoint | Purpose | Protocol |
|----------|---------|----------|
| **`/mcp`** (POST) | **Primary MCP endpoint** | JSON-RPC 2.0 (Standard) |
| `/sse` (GET) | SSE session creation | Server-Sent Events (Legacy) |
| `/message` (POST) | Message handler with session | JSON-RPC 2.0 (Legacy) |
| `/health` (GET) | Health check | JSON |

## Troubleshooting

### LM Studio Cannot Connect

1. ✅ **Verify Server is Running**

   ```bash
   curl -s http://localhost:3344/health
   # Should respond: {"status": "ok"}
   ```

2. ✅ **Check Firewall/Network**

   ```bash
   # From LM Studio machine, try:
   curl -s http://your-server-ip:3344/mcp -X POST -d '{}'
   ```

3. ✅ **Review mcp.json Format**
   - Ensure valid JSON syntax
   - Check URL is correct
   - Use lowercase `"type": "http"`

4. ✅ **View Server Logs**

   ```bash
   # Terminal where server is running should show MCP requests
   # Look for: "MCP method:" log entries
   ```

### Tools Not Available

1. Test with:

   ```bash
   curl -X POST http://localhost:3344/mcp \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
   ```

2. If no tools are listed, check:
   - Server logs for errors
   - All dependencies installed: `pip install -r requirements.txt`
   - Python asyncio not blocked

## Docker Deployment

For Docker container access from LM Studio:

```bash
# Run container with port mapping
docker run -p 3344:3344 \
  --env-file .env \
  --name mcp-tools-server \
  mcp-tools-server:latest
```

Update `mcp.json`:

```json
{
  "mcpServers": {
    "mcp-tools-server": {
      "url": "http://docker-host-ip:3344/mcp",
      "type": "http"
    }
  }
}
```

## Support

For issues, check:

- [MCP Specification](https://modelcontextprotocol.io/spec)
- [LM Studio Documentation](https://lmstudio.ai)
- Server logs at runtime
- Test tools independently using curl
