import os
import httpx
from dotenv import load_dotenv
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

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
async def send_sms(message: str, recipient: str) -> str:
    """Send an SMS message to a phone number"""
    if not APP_ID or not APP_SECRET or not SENDER_ID:
        raise ToolError(
            "SMS configuration missing: AppID, AppSecret, or SENDER_ID environment variable is not set."
        )
    token = f"{APP_ID}.{APP_SECRET}"
    async with httpx.AsyncClient() as client:
        response = await client.post(
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
    raise ToolError(
        f"SMS API returned {response.status_code}: {response.text}"
    )