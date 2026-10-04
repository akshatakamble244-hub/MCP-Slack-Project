import asyncio
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():

    # MCP Server configuration
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=None
    )

    # Connect to MCP Server
    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            # Initialize MCP Server
            await session.initialize()

            # Get available tools
            tools = await session.list_tools()

            print("\nAvailable MCP Tools:")

            for tool in tools.tools:
                print("-", tool.name)

            # --------------------------------
            # Test Weather Tool
            # --------------------------------

            city = input("\nEnter city for weather: ")

            weather_result = await session.call_tool(
                "weather",
                arguments={
                    "city": city
                }
            )

            print("\nWeather Result:")
            print(weather_result)

            # --------------------------------
            # Send Slack Message
            # --------------------------------

            message = input("\nEnter your Slack message: ")

            send_result = await session.call_tool(
                "send_message",
                arguments={
                    "message": message
                }
            )

            print("\nSlack Send Result:")
            print(send_result)

            # --------------------------------
            # Read Slack Messages
            # --------------------------------

            read_result = await session.call_tool(
                "read_messages",
                arguments={
                    "limit": 5
                }
            )

            print("\nLatest Slack Messages:")
            print(read_result)


if __name__ == "__main__":
    asyncio.run(main())