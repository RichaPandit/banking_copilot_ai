
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Dict, Any
import os, logging
from datetime import datetime, timezone
import pandas as pd

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal
from mcp.server.fastmcp import FastMCP, Context
from starlette.routing import Mount

# -----------------
# FastAPI app
# -----------------
app = FastAPI(
    title="Banking MCP Server",
    description="MCP Server for Banking Risk Intelligence Agent",
    version="1.0",
    debug=True,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# -----------------
# CSV data (if needed for tools)
# -----------------
companies   = load_csv("data/companies.csv")
financials  = load_csv("data/financials.csv")
exposure    = load_csv("data/exposure.csv")
covenants   = load_csv("data/covenants.csv")
ews         = load_csv("data/ews.csv")

# -----------------
# Helpers
# -----------------
AGENT_HEADER      = "x-agent-key"
AGENT_HEADER_ALT  = AGENT_HEADER.replace("-", "_")
DEFAULT_LIST_LIMIT = 50
MAX_LIST_LIMIT     = 200

def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)
    return agent_id

# -----------------
# MCP adapter + tools
# -----------------
mcp_adapter = FastMCP("Banking MCP")

# 1) Ping — use decorator ONLY (remove add_tool(ping))
@mcp_adapter.tool()
def ping() -> dict:
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}

# 2) Companies
@mcp_adapter.tool()
def mcp_get_companies(context: Context, limit: int = DEFAULT_LIST_LIMIT, offset: int = 0) -> list[dict]:
    lim = min(max(limit, 1), MAX_LIST_LIMIT)
    return companies.iloc[offset: offset + lim].to_dict(orient="records")

# 3) Financials
@mcp_adapter.tool()
def mcp_get_financials(context: Context, company_id: str) -> list[dict]:
    df = financials[financials["company_id"] == company_id]
    return df.to_dict(orient="records")

# 4) Exposure
@mcp_adapter.tool()
def mcp_get_exposure(context: Context, company_id: str) -> list[dict]:
    df = exposure[exposure["company_id"] == company_id]
    return df.to_dict(orient="records")

# 5) Covenants
@mcp_adapter.tool()
def mcp_get_covenants(context: Context, company_id: str) -> list[dict]:
    df = covenants[covenants["company_id"] == company_id]
    return df.to_dict(orient="records")

# 6) EWS
@mcp_adapter.tool()
def mcp_get_ews(context: Context, company_id: str) -> list[dict]:
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

# 7) Generate report wrapper
@mcp_adapter.tool()
def generate_report_wrapper(context: Context, company_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    request = {"company_id": company_id}
    if isinstance(params, dict):
        request.update(params)
    try:
        result = generate_report_internal(request)
    except TypeError:
        result = generate_report_internal(company_id)
    if isinstance(result, pd.DataFrame):
        return {"rows": result.to_dict(orient="records")}
    if isinstance(result, dict):
        return result
    return {"result": str(result)}

# -----------------
# Mount MCP ASGI sub-app (robust to slash variants)
# -----------------
mcp_app = mcp_adapter.streamable_http_app()

# Prevent slash redirect (avoids 307 bounce /mcp -> /mcp/)
app.router.redirect_slashes = False

# Mount canonical path and trailing-slash variant
app.mount("/mcp", mcp_app)
app.router.routes.append(Mount(path="/mcp/", app=mcp_app))

# -----------------
# (Optional) include your existing FastAPI routers
# -----------------
if tools_router is not None:
    app.include_router(tools_router)

# -----------------
# Local run for testing (optional)
# -----------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
