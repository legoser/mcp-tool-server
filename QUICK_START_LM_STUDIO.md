# 🚀 Quick Start: LM Studio + MCP Tools Server

## 1. Start the MCP Server

```bash
# Terminal 1: Start server with /mcp endpoint
python -m uvicorn src.main_sse:app --port 3344

# You should see:
# INFO:     Started server process [XXXX]
# INFO:     Uvicorn running on http://0.0.0.0:3344
```

## 2. Verify Server is Running

```bash
# Terminal 2: Quick test
curl -s http://localhost:3344/health
# Expected: {"status": "ok"}
```

## 3. Configure LM Studio

### Find Config Directory

- **macOS**: Open Finder → Go → Go to Folder → `~/Library/Application Support/LMStudio`
- **Linux**: `~/.config/LMStudio` or `~/.local/share/LMStudio`
- **Windows**: `%APPDATA%\LMStudio`

### Create/Edit `mcp.json`

Create file `mcp.json` in the config directory with this content:

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

### For Remote Server

Replace `localhost` with your server IP/hostname:

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

## 4. Restart LM Studio

- Quit LM Studio completely
- Reopen LM Studio

## 5. Verify Connection

In LM Studio settings, under "Model Context Protocol (MCP)":

✅ **Success** — You should see:

- `mcp-tools-server` listed
- Status shows "Connected"

❌ **Troubleshooting** — If not connected:

- Check JSON syntax in `mcp.json` (use Prettier or similar)
- Verify server is running: `curl http://localhost:3344/health`
- Check LM Studio logs
- Ensure firewall allows port 3344

## 6. Use Tools in Chat

Now you can ask the model to use tools:

**Example prompts:**

- "What time is it?"
- "Tell me a joke"
- "Search the web for python asyncio"
- "Get current weather"

The model will automatically use the available tools!

## Available Tools

Once connected, these tools are available:

| Tool | What it does |
|------|-------------|
| `get_current_time` | Current time (MSK) |
| `get_random_joke` | Random joke |
| `get_random_quote` | Random quote |
| `get_random_fact` | Random fact |
| `web_search` | Search the internet |
| `web_fetch` | Load and read web pages |
| `get_weather` | Get weather data |
| `generate_text` | Generate text (Ollama) |
| `chat_with_ai` | Chat with AI (Ollama) |
| `list_ollama_models` | List Ollama models |

## Help

- See [LM_STUDIO_SETUP.md](LM_STUDIO_SETUP.md) for detailed setup
- See [PROTOCOL_MIGRATION.md](PROTOCOL_MIGRATION.md) for technical details
- Test endpoint: `./test_mcp_endpoint.sh`
