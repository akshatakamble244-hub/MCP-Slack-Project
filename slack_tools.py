import os
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()

slack_client = WebClient(
    token=os.getenv("SLACK_BOT_TOKEN")
)

CHANNEL_ID = "C0C69HSSNPM"


def send_slack_message(message: str):
    response = slack_client.chat_postMessage(
        channel=CHANNEL_ID,
        text=message
    )

    return {
        "success": True,
        "message": response["message"]["text"]
    }


def read_slack_messages(limit: int = 10):
    try:
        response = slack_client.conversations_history(
            channel=CHANNEL_ID,
            limit=limit
        )

        messages = []

        for message in response["messages"]:
            messages.append({
                "user": message.get("user", "Unknown"),
                "text": message.get("text", "")
            })

        return {
            "success": True,
            "messages": messages
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }