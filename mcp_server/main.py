from typing import Any, Dict, List
import os
import logging
import httpx
import requests
import json

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import generate_report_internal, escalate_alert_internal

# FastMCP (MVP-style imports)
from fastmcp.server import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.http import create_streamable_http_app
from fastmcp.server.context import Context

# ToolError may live under fastmcp.server.exceptions; provide a safe fallback
try:
    from fastmcp.server.exceptions import ToolError  # type: ignore
except Exception:  # pragma: no cover
    class ToolError(Exception):
        pass

DEFAULT_LIST_LIMIT = 50
MAX_LIST_LIMIT = 200
TOP_N = int(os.getenv("MCP_RESOURCE_TOP_N", "4"))
# -----------------
# CSV data
# -----------------
companies   = load_csv("data/companies.csv")
financials  = load_csv("data/financials.csv")
exposure    = load_csv("data/exposure.csv")
covenants   = load_csv("data/covenants.csv")
ews         = load_csv("data/ews.csv")

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

def _get_agent_id_from_headers() -> str:
    """
    Extract an agent ID from headers.
    We accept either `x-agent-id` or `x-agent-key` with optional 'Bearer ' prefix.
    """
    headers = get_http_headers()
    agent = headers.get("x-agent-id") or headers.get("x-agent-key") or ""
    if isinstance(agent, str) and agent.lower().startswith("bearer "):
        agent = agent[7:].strip()
    return agent

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

# ------------------------
# Resources
# ------------------------
@mcp.resource("data://companies", name="Companies",
              description="List of corporate borrowers (company_id, company_name, sector)",
              mime_type="application/json")
def res_companies() -> List[Dict]:
    # Concrete resource: no parameters and no URI placeholders
    return companies.iloc[:DEFAULT_LIST_LIMIT].to_dict(orient="records")

@mcp.resource("data://financials/{company_id}", name="Financials",
              description="Income statement and balance sheet time series",
              mime_type="application/json")
def res_financials(company_id: str) -> List[Dict]:
    df = financials[financials["company_id"] == company_id]
    return df.to_dict(orient="records")

@mcp.resource("data://exposure/{company_id}", name="Exposure",
              description="Sanctioned limit, utilized amount, overdue, collateral, DPD",
              mime_type="application/json")
def res_exposure(company_id: str) -> List[Dict]:
    df = exposure[exposure["company_id"] == company_id]
    return df.to_dict(orient="records")

@mcp.resource("data://covenants/{company_id}", name="Covenants",
              description="Covenant thresholds and last actuals",
              mime_type="application/json")
def res_covenants(company_id: str) -> List[Dict]:
    df = covenants[covenants["company_id"] == company_id]
    return df.to_dict(orient="records")

@mcp.resource("data://ews/{company_id}", name="EarlyWarningSignals",
              description="Early warning signal events",
              mime_type="application/json")
def res_ews(company_id: str) -> List[Dict]:
    df = ews[ews["company_id"] == company_id]
    return df.to_dict(orient="records")

# ----------------------------------------
# Materialize top-N concrete resources
# ----------------------------------------
def register_featured_resources() -> None:
    featured = os.getenv("MCP_RESOURCE_FEATURED_ID", "").strip()
    if not featured:
        return
    
    if companies.empty or not (companies["company_id"].astype(str)==featured).any():
        logger.warning("Featured company_id '%s' not found in companies.csv", featured)
        return

    # Helper factories that return **parameterless** functions (no arguments!)
    def make_fin_reader(cid: str):
        def fin_reader() -> List[Dict]:
            df = financials[financials["company_id"] == cid]
            return df.to_dict(orient="records")
        return fin_reader

    def make_exp_reader(cid: str):
        def exp_reader() -> List[Dict]:
            df = exposure[exposure["company_id"] == cid]
            return df.to_dict(orient="records")
        return exp_reader

    def make_cov_reader(cid: str):
        def cov_reader() -> List[Dict]:
            df = covenants[covenants["company_id"] == cid]
            return df.to_dict(orient="records")
        return cov_reader

    def make_ews_reader(cid: str):
        def ews_reader() -> List[Dict]:
            df = ews[ews["company_id"] == cid]
            return df.to_dict(orient="records")
        return ews_reader
    
    cid = featured
    
    mcp.resource(
        f"data://financials/{cid}",
        name=f"Financials",
        description=f"Financials for {cid}",
        mime_type="application/json"
    )(make_fin_reader(cid))

    mcp.resource(
        f"data://exposure/{cid}",
        name=f"Exposure",
        description=f"Financials for {cid}",
        mime_type="application/json"
    )(make_exp_reader(cid))

    mcp.resource(
        f"data://covenants/{cid}",
        name=f"Covenants",
        description=f"Covenants for {cid}",
        mime_type="application/json"
    )(make_cov_reader(cid))

    mcp.resource(
        f"data://ews/{cid}",
        name=f"EWS",
        description=f"Early Warning Signals for {cid}",
        mime_type="application/json"
    )(make_ews_reader(cid))

try:
    register_featured_resources()
except Exception as e:
    logger.exception("Feature resource registration failed: %s", e)

#----------------------
# Tools
# --------------------------
@mcp.tool()
async def generate_report(company_id: str) -> str:
    """
    MCP tool that generates the Word/PDF report by delegating to tools.py.
    Returns: {"status", "company", "risk_score", "risk_rating", "word_report", "pdf_report", "rag_highlights"}
    """
    
    x_agent_id = _get_agent_id_from_headers()
    result: Dict[str, Any] = generate_report_internal(
        company_id=company_id,
        x_agent_id=x_agent_id,
        companies=companies,
        financials=financials,
        exposure=exposure,
        covenants=covenants,
        ews=ews,
    )
    # Return as JSON string, which FastMCP will emit as a text content block
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def escalate_alert(context: Context, company_id: str) -> str:
    """
    Escalate to Microsoft Teams via Workflows webhook.
    Returns a JSON string with status/code/message.
    """
    x_agent_id = _get_agent_id_from_headers()

    # (Optionally) fetch current risk info to include in the card
    # For now, we pass None; you can pass real scores from your CSVs or report result
    result = escalate_alert_internal(
        company_id=company_id,
        x_agent_id=x_agent_id,
        risk_score=None,
        risk_rating=None,    
        extra={}
    )
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def get_company_context(company_id: str) -> str:
    """
    Return all company context (financials, exposure, covenants, ews) in one JSON string
    so Copilot Studio can deterministically consume it in a Topic.
    """
    ctx = {
        "company_id": company_id,
        "financials": res_financials(company_id),   # uses your resource function
        "exposure":   res_exposure(company_id),
        "covenants":  res_covenants(company_id),
        "ews":        res_ews(company_id),
    }
    return json.dumps(ctx, ensure_ascii=False)

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