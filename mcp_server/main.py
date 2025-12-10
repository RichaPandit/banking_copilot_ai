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

JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"
AGENT_HEADER: str = "x-agent-key"
AGENT_HEADER_ALT: str = AGENT_HEADER.replace('-', '_')
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50
DEV_ASSUME_KEY: Optional[str] = os.getenv("MCP_DEV_ASSUME_KEY")

app = FastAPI(title="Banking MCP Server", description="MCP Server for Banking Risk Intelligence Agent", version="1.0", debug=True)
manifest_path = os.path.join("copilot_integration","copilot_manifest.json")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

# CORS
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# -----------------
# Data bootstrap
# -----------------
companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure = load_csv("data/exposure.csv")
covenants = load_csv("data/covenants.csv")
ews = load_csv("data/ews.csv")

# -----------------
# Health & root
# -----------------
@app.get("/health")
def health():
    return {"status": "ok", "variant": "mcp-streamable", "dev_assume_key": bool(DEV_ASSUME_KEY)}

@app.get("/")
def root_probe():
    # Advertise the canonical MCP endpoint with a trailing slash
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp/", "variant": "streamable-http"}

# -------------
# MCP: mount official Streamable HTTP sub-app at /mcp (stateless)
# -------------
# Sub-app serves at its own root ('/'); we mount it at '/mcp' on FastAPI.
# Stateless mode avoids session-manager task group initialization.

mcp_adapter = FastMCP("Banking MCP")
app.mount("/mcp/", mcp_adapter.streamable_http_app())

# TEMP: route dump to verify /mcp appears in logs
for r in app.routes:
    try:
        logger.info("ROUTE MOUNTED: %s", getattr(r, "path", r))
    except Exception:
        pass

# Optional: redirect legacy root POSTs straight to canonical /mcp/
@app.post("/")
async def legacy_root_redirect():
    return RedirectResponse(url="/mcp/", status_code=307)

@mcp_adapter.tool()
def ping() -> dict:
    return {"ok": True, "ts": datetime.now(timezone.utc).replace("+00:00", "Z")}

mcp_adapter.add_tool("ping", ping)
# 3) Add a diag endpoint to confirm MCP SDK version (ensures stateless_http is supported).
import mcp as mcp_pkg

@app.get("/diag/mcp-methods")
def diag_mcp_methods():
    return {"FastMCP_dir": dir(FastMCP),
            "adapter_dir": dir(mcp_adapter)
            }

# -----------------
# REST fallback endpoints (unchanged behavior)
# -----------------

def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)
    return agent_id

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

# Keep your existing tools router (e.g., /tools/generate-report/{company_id})
app.include_router(tools_router)
