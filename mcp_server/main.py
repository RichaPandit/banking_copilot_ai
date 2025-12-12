from typing import Any
import os
import logging
import httpx
import requests

# FastMCP (MVP-style imports)
from fastmcp.server import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.http import create_streamable_http_app

# ToolError may live under fastmcp.server.exceptions; provide a safe fallback
try:
    from fastmcp.server.exceptions import ToolError  # type: ignore
except Exception:  # pragma: no cover
    class ToolError(Exception):
        pass

# ---------------------------------------------------------------------------
# Tokens from environment (Azure App Service)
# ---------------------------------------------------------------------------
# Primary token for Copilot Studio -> MCP auth
LOCAL_TOKEN: str = os.getenv("MCP_DEV_ASSUME_KEY", os.getenv("LOCAL_TOKEN", "")).strip()
# Optional external API token if you later call an API like OutScraper
API_TOKEN: str = os.getenv("API_TOKEN", "").strip()

HEADER_NAME = "x-agent-key"  # Aligns with your manifest

# ---------------------------------------------------------------------------
# Authentication middleware (MVP pattern)
# ---------------------------------------------------------------------------
class UserAuthMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        # Extract headers from current HTTP request (works in Streamable HTTP)
        headers = get_http_headers()

        # Accept the manifest header name; also accept 'api-key' for flexibility
        mcp_api_key = headers.get(HEADER_NAME) or headers.get("api-key")
        if not mcp_api_key:
            raise ToolError("Access denied: no key provided")

        if not mcp_api_key.startswith("Bearer "):
            logging.info("invalid token format in %s", HEADER_NAME)
            raise ToolError("Access denied: invalid token format")

        token = mcp_api_key.removeprefix("Bearer ").strip()
        expected = (LOCAL_TOKEN or "").strip()
        if not expected:
            raise ToolError("Access denied: server not configured")
        if token != expected:
            raise ToolError("Access denied: invalid token")

        return await call_next(context)

# ---------------------------------------------------------------------------
# Initialize FastMCP server (Streamable HTTP, JSON responses)
# ---------------------------------------------------------------------------
# json_response=True disables SSE; Streamable HTTP works well with proxies
mcp = FastMCP(
    name="CreditRiskCopilotAgent",
    json_response=True,
    stateless_http=True,
)

# Attach middleware
mcp.add_middleware(UserAuthMiddleware())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Sample resource (optional)
# ---------------------------------------------------------------------------
@mcp.resource("file://app.log")
def get_log_file() -> str:
    """Returns the application log file contents"""
    try:
        with open("app.log", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "app.log not found"

# ---------------------------------------------------------------------------
# Sample tools (replace with your banking tools as needed)
# ---------------------------------------------------------------------------
@mcp.tool()
async def ping() -> str:
    return "pong"

@mcp.tool()
async def generate_report(company_id: str) -> str:
    # Placeholder: replace with your actual report generation
    return f"Report generated for {company_id}"

# Example of calling an external API (kept similar to MVP style)
@mcp.tool()
async def get_external_reviews(query: str) -> str:
    """Example external call (disabled if API_TOKEN missing)."""
    if not API_TOKEN:
        return "External API token not configured"

    api_url = (
        "https://api.app.outscraper.com/maps/reviews-v3?"
        f"query={query}&async=false&reviewsLimit=5"
    )
    headers = {
        "x-api-key": API_TOKEN,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.get(api_url, headers=headers, timeout=20)
        resp.raise_for_status()
        return str(resp.json())
    except requests.exceptions.RequestException as e:
        logger.exception("Error calling external API")
        return f"Error calling API: {e}"

# ---------------------------------------------------------------------------
# ASGI app for Azure App Service (gunicorn) and direct run fallback
# ---------------------------------------------------------------------------
# Expose an ASGI app so you can use gunicorn: `gunicorn -k uvicorn.workers.UvicornWorker main:app`
app = create_streamable_http_app(
    server=mcp,
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    debug=False,
)

if __name__ == "__main__":
    # Optional: direct run — useful on platforms that execute the script directly
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    # path=/mcp is the default for Streamable HTTP; set explicitly for clarity
    mcp.run(transport="streamable-http", host=host, port=port, path="/mcp")