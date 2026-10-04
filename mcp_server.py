from mcp.server.mcpserver import MCPServer

from slack_tools import send_slack_message, read_slack_messages
from weather_tools import get_weather


# Create MCP Server
server = MCPServer("MCP Slack Assistant")


# --------------------------------
# Slack: Send Message
# --------------------------------

@server.tool()
async def send_message(message: str) -> dict:
    """
    Send a message to the Slack #new-channel.
    """
    return send_slack_message(message)


# --------------------------------
# Slack: Read Messages
# --------------------------------

@server.tool()
async def read_messages(limit: int = 10) -> dict:
    """
    Read recent messages from Slack #new-channel.
    """
    return read_slack_messages(limit)


# --------------------------------
# Weather
# --------------------------------

@server.tool()
async def weather(city: str) -> dict:
    """
    Get current weather information for a city.
    """
    return get_weather(city)


# --------------------------------
# Start MCP Server
# --------------------------------

if __name__ == "__main__":
    server.run()