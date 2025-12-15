
from typing import Any, Dict, List
import os
import logging
import json

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import generate_report_internal, escalate_alert_internal

# FastMCP
from fastmcp.server import FastMCP
from fastmcp.server.dependencies import get_http_headers
from fastmcp.server.middleware import Middleware, MiddlewareContext
from fastmcp.server.http import create_streamable_http_app
from fastmcp.server.context import Context

try:
    from fastmcp.server.exceptions import ToolError  # type: ignore
except Exception:
    class ToolError(Exception):
        pass

# -----------------
# Config & constants
# -----------------
DEFAULT_LIST_LIMIT = 50
MAX_LIST_LIMIT = 200
HEADER_NAME = "x-agent-key"

# -----------------
# CSV data
# -----------------
companies  = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure   = load_csv("data/exposure.csv")
covenants  = load_csv("data/covenants.csv")
ews        = load_csv("data/ews.csv")

# -----------------
# Tokens
# -----------------
LOCAL_TOKEN: str = os.getenv("MCP_DEV_ASSUME_KEY", os.getenv("LOCAL_TOKEN", "")).strip()
API_TOKEN:  str = os.getenv("API_TOKEN", "").strip()

# -----------------
# Auth middleware
# -----------------
class UserAuthMiddleware(Middleware):
    async def on_message(self, context: MiddlewareContext, call_next):
        headers = get_http_headers()

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
    Accept either `x-agent-id` or `x-agent-key` with optional 'Bearer ' prefix.
    """
    headers = get_http_headers()
    agent = headers.get("x-agent-id") or headers.get("x-agent-key") or ""
    if isinstance(agent, str) and agent.lower().startswith("bearer "):
        agent = agent[7:].strip()
    return agent

# -----------------
# FastMCP app
# -----------------
mcp = FastMCP(
    name="CreditRiskCopilotAgent",
    json_response=True,
    stateless_http=True,
)
mcp.add_middleware(UserAuthMiddleware())

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -----------------
# Internal data helpers (single source of truth)
# -----------------
def _financials_for(company_id: str) -> List[Dict]:
    df = financials[financials["company_id"] == company_id]
    return df.to_dict(orient="records")

def _exposure_for(company_id: str) -> List[Dict]:
    df = exposure[exposure["company_id"] == company_id]
    return df.to_dict(orient="records")

def _covenants_for(company_id: str) -> List[Dict]:
    df = covenants[covenants["company_id"] == company_id]
    return df.to_dict(orient="records")

def _ews_for(company_id: str) -> List[Dict]:
    df = ews[ews["company_id"] == company_id]
    return df.to_dict(orient="records")

# ------------------------
# RESOURCES
# ------------------------

@mcp.resource("data://companies", name="Companies",
              description="List of corporate borrowers (company_id, company_name, sector)",
              mime_type="application/json")
def res_companies() -> List[Dict]:
    # Concrete resource (fixed URI, no params)
    return companies.iloc[:DEFAULT_LIST_LIMIT].to_dict(orient="records")

@mcp.resource("data://financials/{company_id}", name="Financials",
              description="Income statement and balance sheet time series",
              mime_type="application/json")
def res_financials(company_id: str) -> List[Dict]:
    return _financials_for(company_id)

@mcp.resource("data://exposure/{company_id}", name="Exposure",
              description="Sanctioned limit, utilized amount, overdue, collateral, DPD",
              mime_type="application/json")
def res_exposure(company_id: str) -> List[Dict]:
    return _exposure_for(company_id)

@mcp.resource("data://covenants/{company_id}", name="Covenants",
              description="Covenant thresholds and last actuals",
              mime_type="application/json")
def res_covenants(company_id: str) -> List[Dict]:
    return _covenants_for(company_id)

@mcp.resource("data://ews/{company_id}", name="EarlyWarningSignals",
              description="Early warning signal events",
              mime_type="application/json")
def res_ews(company_id: str) -> List[Dict]:
    return _ews_for(company_id)

# ----------------------------------------
# Materialize 4 concrete resources for ONE featured company
# ----------------------------------------
def register_featured_resources() -> None:
    featured = os.getenv("MCP_RESOURCE_FEATURED_ID", "").strip()
    if not featured:
        return

    if companies.empty or not (companies["company_id"].astype(str) == featured).any():
        logger.warning("Featured company_id '%s' not found in companies.csv", featured)
        return

    def make_fin_reader(cid: str):
        def fin_reader() -> List[Dict]:
            return _financials_for(cid)
        return fin_reader

    def make_exp_reader(cid: str):
        def exp_reader() -> List[Dict]:
            return _exposure_for(cid)
        return exp_reader

    def make_cov_reader(cid: str):
        def cov_reader() -> List[Dict]:
            return _covenants_for(cid)
        return cov_reader

    def make_ews_reader(cid: str):
        def ews_reader() -> List[Dict]:
            return _ews_for(cid)
        return ews_reader

    cid = featured

    mcp.resource(
        f"data://financials/{cid}",
        name=f"Financials {cid}",
        description=f"Financials for {cid}",
        mime_type="application/json",
    )(make_fin_reader(cid))

    mcp.resource(
        f"data://exposure/{cid}",
        name=f"Exposure {cid}",
        description=f"Exposure for {cid}",
        mime_type="application/json",
    )(make_exp_reader(cid))

    mcp.resource(
        f"data://covenants/{cid}",
        name=f"Covenants {cid}",
        description=f"Covenants for {cid}",
        mime_type="application/json",
    )(make_cov_reader(cid))

    mcp.resource(
        f"data://ews/{cid}",
        name=f"EWS {cid}",
        description=f"Early Warning Signals for {cid}",
        mime_type="application/json",
    )(make_ews_reader(cid))

try:
    register_featured_resources()
except Exception as e:
    logger.exception("Featured resource registration failed: %s", e)

# --------------------------
# TOOLS
# --------------------------

@mcp.tool()
async def generate_report(company_id: str) -> str:
    """
    Generate a Word/PDF risk report by delegating to tools.py.
    Returns JSON string: {"status","company","risk_score","risk_rating","word_report","pdf_report","rag_highlights"}.
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
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def escalate_alert(context: Context, company_id: str) -> str:
    """
    Escalate to Microsoft Teams via Workflows webhook (configured in tools.py).
    Returns JSON: {"status","code","message"}.
    """
    x_agent_id = _get_agent_id_from_headers()
    
    latest_report = generate_report_internal(
        company_id=company_id,
        x_agent_id=x_agent_id,
        companies=companies,
        financials=financials,
        exposure=exposure,
        covenants=covenants,
        ews=ews,
    )

    result = escalate_alert_internal(
        company_id=company_id,
        x_agent_id=x_agent_id,
        risk_score= latest_report.get("risk_score"),
        risk_rating=latest_report.get("risk_rating"),
        extra={"report_url": latest_report.get("word_report_url")}
    )
    return json.dumps(result, ensure_ascii=False)

@mcp.tool()
def get_company_context(company_id: str) -> str:
    """
    Return all company context (financials, exposure, covenants, ews) as one JSON string
    so Copilot Studio can consume it deterministically in a Topic.
    """
    ctx = {
        "company_id": company_id,
        "financials": _financials_for(company_id),
        "exposure":   _exposure_for(company_id),
        "covenants":  _covenants_for(company_id),
        "ews":        _ews_for(company_id),
    }
    return json.dumps(ctx, ensure_ascii=False)

# --------------------------
# ASGI app & direct run
# --------------------------
app = create_streamable_http_app(
    server=mcp,
    streamable_http_path="/mcp",
    json_response=True,
    stateless_http=True,
    debug=False,
)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    mcp.run(transport="streamable-http", host=host, port=port, path="/mcp")