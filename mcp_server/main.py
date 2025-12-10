from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response, JSONResponse, RedirectResponse
from typing import Optional, Dict, Any
import logging, json, os
from datetime import datetime, timezone
import pandas as pd

# Project-local utilities/routers (keep your existing behavior)
from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal
# MCP SDK (official) – use ASGI sub-app for Streamable HTTP in stateless mode
from mcp.server.fastmcp import FastMCP, Context
# Add a diag endpoint to confirm MCP SDK version (ensures stateless_http is supported).
import mcp as mcp_pkg

#-------------------
# Constants & Config
#-------------------
JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"
AGENT_HEADER: str = "x-agent-key"
AGENT_HEADER_ALT: str = AGENT_HEADER.replace('-', '_')
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50
DEV_ASSUME_KEY: Optional[str] = os.getenv("MCP_DEV_ASSUME_KEY")
manifest_path = os.path.join("copilot_integration","copilot_manifest.json")

#-------------------
# FASTAPI App
#-------------------
app = FastAPI(
    title="Banking MCP Server",
    description="MCP Server for Banking Risk Intelligence Agent",
    version="1.0",
    debug=True)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# -----------------
# Load CSV Data
# -----------------
companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure = load_csv("data/exposure.csv")
covenants = load_csv("data/covenants.csv")
ews = load_csv("data/ews.csv")

# -----------------
# REST: Health & Root
# -----------------
@app.get("/health")
def health():
    return {"status": "ok", "variant": "mcp-streamable", "dev_assume_key": bool(DEV_ASSUME_KEY)}

@app.get("/")
def root_probe():
    # Advertise the canonical MCP endpoint with a trailing slash
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp/", "variant": "streamable-http"}

@app.post("/")
async def legacy_root_redirect():
    return RedirectResponse(url="/mcp/", status_code=307)

def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)
    return agent_id

# -----------------
# REST: resource endpoints
# -----------------
@app.get("/copilot_manifest.json")
async def get_manifest():
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    return JSONResponse(content=manifest)

@app.get("/resources/companies")
def get_companies_endpoint(x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT), limit: int = DEFAULT_LIST_LIMIT, offset: int = 0):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    lim = min(max(limit, 1), MAX_LIST_LIMIT)
    return companies.iloc[offset: offset + lim].to_dict(orient="records")

@app.get("/resources/financials/{company_id}")
def get_financials_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = financials[financials["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/exposure/{company_id}")
def get_exposure_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = exposure[exposure["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/covenants/{company_id}")
def get_covenants_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = covenants[covenants["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/ews/{company_id}")
def get_ews_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

# -----------------
# REST: Tool endpoints
# -----------------
@app.post("/tools/generate-report/{company-id}")
def rest_generate_report(company_id: str,
                         payload: Optional[Dict[str, Any]] = None,
                         x_agent_key: Optional[str]= Header(None, alias=AGENT_HEADER),
                         x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    request = {"company_id": company_id}
    if isinstance(payload,dict):
        request.update(payload)
    result = generate_report_internal(request)
    if isinstance(result, pd.DataFrame):
        return result.to_dict(orient="records")
    return result

@app.post("/tools/escalate-alert/{company-id}")
def rest_escalate_alert(company_id: str,
                         x_agent_key: Optional[str]= Header(None, alias=AGENT_HEADER),
                         x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    _ = resolve_agent_id(x_agent_key, x_agent_key_alt)
    now = datetime.now(timezone.utc).isoformat()
    return {"status": "escalated", "company_id": company_id, "escalated_at": now}

# -------------
# MCP: Streamable HTTP sub-app setup
# -------------
mcp_adapter = FastMCP("Banking MCP")

# ---- Define MCP Tools ----

# 1). Ping
@mcp_adapter.tool()
def ping() -> dict:
    return {"ok": True, "ts": datetime.now(timezone.utc).isoformat()}
mcp_adapter.add_tool(ping)

def mcp_get_companies(context: Context, limit: int = DEFAULT_LIST_LIMIT, offset: int =0) -> list[dict]:
    lim = min(max(limit,1), MAX_LIST_LIMIT)
    return companies.iloc[offset: offset+lim].to_dict(orient="records")
mcp_adapter.add_tool(mcp_get_companies)

# 2). Financials
def mcp_get_financials(context: Context, company_id: str) -> list[dict]:
    df = financials[financials["company_id"] == company_id]
    return df.to_dict(orient="records")
mcp_adapter.add_tool(mcp_get_financials)

# 3). Exposure
def mcp_get_exposure(context: Context, company_id: str) -> list[dict]:
    df = exposure[exposure["company_id"] == company_id]
    return df.to_dict(orient="records")
mcp_adapter.add_tool(mcp_get_exposure)

# 4). Covenants
def mcp_get_covenants(context: Context, company_id: str) -> list[dict]:
    df = covenants[covenants["company_id"] == company_id]
    return df.to_dict(orient="records")
mcp_adapter.add_tool(mcp_get_covenants)

# 5). Early Warning Signals (EWS)
def mcp_get_ews(context: Context, company_id: str) -> list[dict]:
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")
mcp_adapter.add_tool(mcp_get_ews)

# 6). Generate Report (from existing router function)
def generate_report_wrapper(context: Context, company_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    request = {"company_id": company_id}
    if isinstance(params, dict):
        request.update(params)
    try:
        result = generate_report_internal(request)
    except TypeError:
        result = generate_report_internal(company_id)
    if isinstance(result,pd.DataFrame):
        return{"rows": result.to_dict(orient="records")}
    if isinstance(result,dict):
        return result
    return {"result": str(result)}
mcp_adapter.add_tool(generate_report_wrapper)

# -------------
# Diagnostics
# -------------
@app.get("/diag/mcp-status")
async def diag_mcp_status():
    try:
        tools = await mcp_adapter.list_tools()
        return {
            "tools": [t.name for t in tools],
            "initialized": True
        }
    except Exception as e:
        return {"initialized": False, "error": str(e)}

# ---- Mount MCP Sub-App ----
mcp_app = mcp_adapter.streamable_http_app()
mcp_app.openapi = lambda: {}
app.mount("/mcp/", mcp_app)

# Include Tools Router
if tools_router is not None:
    app.include_router(tools_router)

# -------------
# Diagnostics
# -------------
@app.get("/diag/mcp-methods")
def diag_mcp_methods():
    return {"FastMCP_dir": dir(FastMCP),
            "adapter_dir": dir(mcp_adapter),
            "mcp_version": getattr(mcp_pkg, "__version__", "unknown")
        }