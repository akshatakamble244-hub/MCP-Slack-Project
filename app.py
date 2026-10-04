import streamlit as st
import asyncio
import sys
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="MCP Client Dashboard",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------------------
# MCP Helper Function
# -----------------------------------------

async def call_mcp_tool(tool_name, arguments):

    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            result = await session.call_tool(
                tool_name,
                arguments=arguments
            )

            return result


# -----------------------------------------
# Extract MCP Result
# -----------------------------------------

def extract_result(result):

    try:

        text = result.content[0].text

        return json.loads(text)

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# -----------------------------------------
# Sidebar
# -----------------------------------------

with st.sidebar:

    st.title("🛠️ MCP Tools")

    st.markdown("### ☀️ Get Weather")

    st.markdown("### 💬 Send Slack Message")

    st.markdown("### 📖 Read Slack Messages")

    st.divider()

    st.success("🟢 MCP Server Connected")

    st.caption("MCP Slack Assistant")


# -----------------------------------------
# Main Title
# -----------------------------------------

st.title("🤖 MCP Client Dashboard")

st.write(
    "Interact with your MCP Server using Weather and Slack tools."
)


# -----------------------------------------
# Tabs
# -----------------------------------------

weather_tab, send_tab, read_tab = st.tabs(
    [
        "☀️ Get Weather",
        "💬 Send Slack Message",
        "📖 Read Slack Messages"
    ]
)


# =====================================================
# WEATHER
# =====================================================

with weather_tab:

    st.header("☀️ Get Weather")

    city = st.text_input(
        "City",
        placeholder="Enter city name...",
        key="weather_city"
    )

    if st.button(
        "Get Weather",
        type="primary",
        key="weather_button"
    ):

        if not city.strip():

            st.warning("Please enter a city name.")

        else:

            with st.spinner("Getting weather..."):

                result = asyncio.run(
                    call_mcp_tool(
                        "weather",
                        {
                            "city": city
                        }
                    )
                )

            data = extract_result(result)

            if data.get("success"):

                st.success("Weather received!")

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Temperature",
                        data["temperature"]
                    )

                with col2:

                    st.metric(
                        "Condition",
                        data["condition"]
                    )

                st.info(
                    f"📍 City: {data['city']}"
                )

            else:

                st.error(
                    data.get(
                        "error",
                        "Unable to get weather."
                    )
                )


# =====================================================
# SEND SLACK
# =====================================================

with send_tab:

    st.header("💬 Send Slack Message")

    message = st.text_area(
        "Message",
        placeholder="Type your Slack message here...",
        height=150
    )

    if st.button(
        "Send Message",
        type="primary",
        key="send_button"
    ):

        if not message.strip():

            st.warning("Please enter a message.")

        else:

            with st.spinner("Sending message to Slack..."):

                result = asyncio.run(
                    call_mcp_tool(
                        "send_message",
                        {
                            "message": message
                        }
                    )
                )

            data = extract_result(result)

            if data.get("success"):

                st.success(
                    "✅ Message sent successfully!"
                )

                st.write(
                    f"Message: {data['message']}"
                )

            else:

                st.error(
                    data.get(
                        "error",
                        "Unable to send message."
                    )
                )


# =====================================================
# READ SLACK
# =====================================================

with read_tab:

    st.header("📖 Read Slack Messages")

    limit = st.number_input(
        "Number of messages",
        min_value=1,
        max_value=50,
        value=10
    )

    if st.button(
        "Read Messages",
        type="primary",
        key="read_button"
    ):

        with st.spinner("Reading Slack messages..."):

            result = asyncio.run(
                call_mcp_tool(
                    "read_messages",
                    {
                        "limit": int(limit)
                    }
                )
            )

        data = extract_result(result)

        if data.get("success"):

            st.success(
                "✅ Messages received!"
            )

            messages = data.get(
                "messages",
                []
            )

            if not messages:

                st.info("No messages found.")

            else:

                for message in messages:

                    with st.container():

                        st.markdown(
                            f"**👤 {message['user']}**"
                        )

                        st.write(
                            message["text"]
                        )

                        st.divider()

        else:

            st.error(
                data.get(
                    "error",
                    "Unable to read messages."
                )
            )