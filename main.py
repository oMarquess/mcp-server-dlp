import os
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP

load_dotenv()

APP_ID = os.getenv("AppID")
APP_SECRET = os.getenv("AppSecret")
SENDER_ID = os.getenv("SENDER_ID")

mcp = FastMCP("My Server")

app = mcp.http_app(stateless_http=True)


@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone"""
    return f"Hello, {name}!"


@mcp.tool()
def send_sms(message: str, recipient: str) -> str:
    """Send an SMS message to a phone number"""
    token = f"{APP_ID}.{APP_SECRET}"
    response = httpx.post(
        "https://api.letsfish.africa/v1/sms",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        json={
            "sender_id": SENDER_ID,
            "message": message,
            "recipients": [recipient],
        },
    )
    if response.is_success:
        return f"SMS sent successfully to {recipient}."
    return f"Failed to send SMS: {response.status_code} - {response.text}"