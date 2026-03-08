#!/usr/bin/env python3
"""Interactive API test client for MCP Tools Server."""

import asyncio
import json
import sys
from pathlib import Path

import httpx

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

BASE_URL = "http://localhost:3344"


class MCPTestClient:
    """Interactive test client for MCP API."""

    def __init__(self):
        self.session_id = None
        self.request_id = 1

    async def test_health(self):
        """Test health endpoint."""
        print("\n📋 Testing /health endpoint...")
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{BASE_URL}/health")
            print(f"Status: {resp.status_code}")
            print(f"Response: {resp.json()}")

    async def create_session(self):
        """Create SSE session and get session_id."""
        print("\n🔌 Creating SSE session...")
        try:
            async with httpx.AsyncClient(follow_redirects=True) as client:
                async with client.stream("GET", f"{BASE_URL}/sse") as resp:
                    print(f"Status: {resp.status_code}")
                    async for line in resp.aiter_lines():
                        if line.startswith("data: "):
                            data = json.loads(line[6:])
                            if "sessionId" in data.get("result", {}):
                                self.session_id = data["result"]["sessionId"]
                                print(f"✓ Session created: {self.session_id}")
                                return self.session_id
                    print("✗ No session ID received")
        except Exception as e:
            print(f"✗ Error: {e}")

    async def list_tools(self):
        """List all available tools."""
        if not self.session_id:
            print("✗ No session ID. Run create_session() first.")
            return

        print(f"\n📚 Listing tools (session: {self.session_id[:8]}...)...")
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{BASE_URL}/message?session_id={self.session_id}",
                json={
                    "jsonrpc": "2.0",
                    "id": self.request_id,
                    "method": "tools/list",
                    "params": {},
                },
            )
            self.request_id += 1
            data = resp.json()
            if "error" in data:
                print(f"✗ Error: {data['error']}")
            else:
                tools = data.get("result", {}).get("tools", [])
                print(f"✓ Found {len(tools)} tools:")
                for tool in tools:
                    print(f"  - {tool['name']}: {tool['description'][:50]}...")

    async def call_tool(self, tool_name: str, arguments: dict = None):
        """Call a tool."""
        if not self.session_id:
            print("✗ No session ID. Run create_session() first.")
            return

        if arguments is None:
            arguments = {}

        print(f"\n🔧 Calling tool: {tool_name}")
        print(f"   Arguments: {arguments}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{BASE_URL}/message?session_id={self.session_id}",
                json={
                    "jsonrpc": "2.0",
                    "id": self.request_id,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments,
                    },
                },
            )
            self.request_id += 1

            data = resp.json()
            if "error" in data:
                print(f"✗ Error: {data['error']['message']}")
            else:
                content = data.get("result", {}).get("content", [])
                if content:
                    result_text = content[0].get("text", "")
                    print(f"✓ Result:")
                    # Print first 500 chars, then truncate if needed
                    if len(result_text) > 500:
                        print(f"   {result_text[:500]}...")
                    else:
                        print(f"   {result_text}")

    async def interactive_menu(self):
        """Show interactive menu."""
        while True:
            print("\n" + "=" * 60)
            print("MCP Tools Server - API Test Client")
            print("=" * 60)
            print("\nAvailable commands:")
            print("  1. Health check")
            print("  2. Create session")
            print("  3. List tools")
            print("  4. Get current time")
            print("  5. Get random joke")
            print("  6. Get random quote")
            print("  7. Get random fact")
            print("  8. Web search")
            print("  9. Web fetch")
            print("  10. Generate text (Ollama)")
            print("  11. Chat with AI (Ollama)")
            print("  12. List Ollama models")
            print("  0. Exit")
            print()

            choice = input("Enter command (0-12): ").strip()

            try:
                if choice == "0":
                    print("\nGoodbye! 👋")
                    break
                elif choice == "1":
                    await self.test_health()
                elif choice == "2":
                    await self.create_session()
                elif choice == "3":
                    await self.list_tools()
                elif choice == "4":
                    await self.call_tool("get_current_time")
                elif choice == "5":
                    await self.call_tool("get_random_joke")
                elif choice == "6":
                    await self.call_tool("get_random_quote")
                elif choice == "7":
                    await self.call_tool("get_random_fact")
                elif choice == "8":
                    query = input("Enter search query: ").strip()
                    num_results = input("Enter number of results (default 5): ").strip()
                    await self.call_tool("web_search", {
                        "query": query,
                        "num_results": int(num_results) if num_results else 5,
                    })
                elif choice == "9":
                    url = input("Enter URL: ").strip()
                    await self.call_tool("web_fetch", {"url": url})
                elif choice == "10":
                    prompt = input("Enter prompt: ").strip()
                    await self.call_tool("generate_text", {"prompt": prompt})
                elif choice == "11":
                    system_prompt = input("Enter system prompt: ").strip()
                    user_message = input("Enter user message: ").strip()
                    await self.call_tool("chat_with_ai", {
                        "system_prompt": system_prompt,
                        "user_message": user_message,
                    })
                elif choice == "12":
                    await self.call_tool("list_ollama_models")
                else:
                    print("✗ Invalid command")
            except Exception as e:
                print(f"✗ Error: {e}")
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break

    async def run_automated_tests(self):
        """Run automated test suite."""
        print("\n" + "=" * 60)
        print("Running Automated Tests")
        print("=" * 60)

        # Test 1: Health
        await self.test_health()

        # Test 2: Create session
        await self.create_session()

        if not self.session_id:
            print("✗ Cannot continue without session")
            return

        # Test 3: List tools
        await self.list_tools()

        # Test 4: Call tools
        await self.call_tool("get_current_time")
        await self.call_tool("get_random_quote")
        await self.call_tool("get_random_fact")
        await self.call_tool("list_ollama_models")

        print("\n" + "=" * 60)
        print("✓ Automated tests completed")
        print("=" * 60)


async def main():
    """Main entry point."""
    client = MCPTestClient()

    if len(sys.argv) > 1 and sys.argv[1] == "--auto":
        # Automated tests
        await client.run_automated_tests()
    else:
        # Interactive mode
        await client.interactive_menu()


if __name__ == "__main__":
    asyncio.run(main())
