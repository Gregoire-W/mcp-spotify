import asyncio
import os
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from google.genai import types
from google import genai
 

class MCPClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GOOGLE_GENAI_API_KEY"))

    async def _process_query(self, query: str, session) -> str:

        messages = [
            types.Content(
                role="user", parts=[types.Part(text=query)]
            )
        ]

        mcp_response = await session.list_tools()

        formatted_tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": {
                    "type": tool.inputSchema["type"],
                    "properties": tool.inputSchema["properties"],
                    "required": tool.inputSchema["required"],
                }
            }
            for tool in mcp_response.tools
        ]

        tools = types.Tool(function_declarations=formatted_tools)
        config = types.GenerateContentConfig(tools=[tools])

        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config,
        )

        messages.append(response.candidates[0].content)
        
        for part in response.candidates[0].content.parts:
            if part.function_call:
                tool_name = part.function_call.name
                tool_args = part.function_call.args

                result = await session.call_tool(tool_name, tool_args)
                
                function_response_part = types.Part.from_function_response(
                    name=tool_name,
                    response={"result": result},
                )

                messages.append(types.Content(role="user", parts=[function_response_part]))
            elif part.text:
                pass

        final_response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=config,
            contents=messages,
        )

        print("-"*50)
        print(final_response.text)
        print("-"*50)
        
        return final_response.text

    async def run(self, query: str, server_path: str="http://mcp-server:3000/mcp"):
        print("🚀 Connecting to MCP server...", flush=True)
        async with streamablehttp_client(server_path) as (
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

                result = await self._process_query(query, session)
                return result