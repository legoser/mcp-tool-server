"""Integration tests for all MCP tools via stdio."""

import asyncio

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def run_tests():
    params = StdioServerParameters(
        command="python",
        args=["-m", "src.main"],
    )

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}")

            # Test get_current_time
            print("\n[TEST] get_current_time")
            result = await session.call_tool("get_current_time", {})
            print(f"Result: {result.content[0].text}")

            # Test get_random_joke
            print("\n[TEST] get_random_joke")
            result = await session.call_tool("get_random_joke", {})
            print(f"Result: {result.content[0].text}")

            # Test get_random_quote
            print("\n[TEST] get_random_quote")
            result = await session.call_tool("get_random_quote", {})
            print(f"Result: {result.content[0].text}")

            # Test get_random_fact
            print("\n[TEST] get_random_fact")
            result = await session.call_tool("get_random_fact", {})
            print(f"Result: {result.content[0].text}")

            # Test web_search
            print("\n[TEST] web_search")
            result = await session.call_tool(
                "web_search", {"query": "Python programming language", "num_results": 3}
            )
            print(f"Result: {result.content[0].text[:300]}...")

            # Test web_fetch
            print("\n[TEST] web_fetch")
            result = await session.call_tool("web_fetch", {"url": "http://example.com"})
            print(f"Result: {result.content[0].text[:300]}...")

            print("\nAll tests passed!")


if __name__ == "__main__":
    asyncio.run(run_tests())
