import asyncio

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main():
    print("🚀 Connecting to MCP server...", flush=True)
    # Connect to a streamable HTTP server
    async with streamablehttp_client("http://mcp-server:3000/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        print("✅ Connected!", flush=True)
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            print("🔧 Initializing session...", flush=True)
            await session.initialize()
            
            # List available tools
            print("📋 Listing available tools...", flush=True)
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}", flush=True)
            
            print("\n✨ Client finished successfully!", flush=True)
            await asyncio.sleep(2)  # Wait 2 seconds before closing


if __name__ == "__main__":
    asyncio.run(main())