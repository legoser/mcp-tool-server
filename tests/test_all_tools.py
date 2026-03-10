"""Integration tests for all MCP tools via HTTP."""

import asyncio

from mcp import ClientSession
from mcp.client.http import http_client


async def run_tests():
    """Test all tools and prompts via HTTP transport."""
    async with http_client("http://localhost:3344/mcp") as session:
        await session.initialize()

        # List all tools
        tools = await session.list_tools()
        print("Available tools:")
        for tool in tools.tools:
            print(f"  - {tool.name}")

        # Test time tools
        print("\n[TEST] get_current_time")
        result = await session.call_tool("get_current_time", {})
        print(f"Result: {result.content[0].text}")

        print("\n[TEST] get_random_joke")
        result = await session.call_tool("get_random_joke", {})
        print(f"Result: {result.content[0].text}")

        print("\n[TEST] get_random_quote")
        result = await session.call_tool("get_random_quote", {})
        print(f"Result: {result.content[0].text}")

        print("\n[TEST] get_random_fact")
        result = await session.call_tool("get_random_fact", {})
        print(f"Result: {result.content[0].text}")

        # Test web tools
        print("\n[TEST] web_search")
        result = await session.call_tool(
            "web_search", {"query": "Python programming language", "num_results": 3}
        )
        print(f"Result: {result.content[0].text[:300]}...")

        # Test prompts (agents) - basic tests only
        print("\n--- Testing Prompts ---")

        print("\n[TEST] review_code")
        result = await session.call_prompt("review_code", {"code": "def hello(): pass"})
        print(f"Result: {result.content[0].text[:300]}...")

        print("\n[TEST] debug_error")
        result = await session.call_prompt(
            "debug_error", {"code": "x = 1/0", "error": "ZeroDivisionError"}
        )
        print(f"Result: {result.content[0].text[:300]}...")

        print("\nAll tests passed!")


if __name__ == "__main__":
    asyncio.run(run_tests())
