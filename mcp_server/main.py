
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response, JSONResponse, RedirectResponse
from typing import Optional, Dict, Any
import logging, json, os
from datetime import datetime
import pandas as pd

# Project-local utilities/routers (keep your existing behavior)
from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal

# MCP SDK (official) – use ASGI sub-app for Streamable HTTP
from mcp.server.fastmcp import FastMCP

JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"
AGENT_HEADER: str = "x-agent-key"
AGENT_HEADER_ALT: str = AGENT_HEADER.replace('-', '_')
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50
DEV_ASSUME_KEY: Optional[str] = os.getenv("MCP_DEV_ASSUME_KEY")

app = FastAPI(title="Banking MCP Server", description="MCP Server for Banking Risk Intelligence Agent", version="1.0")
manifest_path = os.path.join("copilot_integration","copilot_manifest.json")

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

# CORS + Request logging
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
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp", "variant": "streamable-http"}

# -------------
# MCP: mount official Streamable HTTP sub-app at /mcp
# -------------
# The MCP sub-app serves at its own root ('/'), and we mount it at '/mcp' in our main FastAPI app.
# This is the supported integration with Streamable HTTP (works with Copilot Studio MCP Preview).

mcp = FastMCP("BankingMCP", json_response=True, stateless_http=True,streamable_http_path="/")

# Register MCP resources (templates) – URIs use a custom scheme 'risk://'
@mcp.resource("risk://companies")
def res_companies() -> str:
    return companies.to_json(orient="records")

@mcp.resource("risk://financials/{company_id}")
def res_financials(company_id: str) -> str:
    df = financials[financials["company_id"] == company_id]
    return df.to_json(orient="records")

@mcp.resource("risk://exposure/{company_id}")
def res_exposure(company_id: str) -> str:
    df = exposure[exposure["company_id"] == company_id]
    return df.to_json(orient="records")

@mcp.resource("risk://covenants/{company_id}")
def res_covenants(company_id: str) -> str:
    df = covenants[covenants["company_id"] == company_id]
    return df.to_json(orient="records")

@mcp.resource("risk://ews/{company_id}")
def res_ews(company_id: str) -> str:
    df = ews[ews["company_id"] == company_id]
    return df.to_json(orient="records")

# Register MCP tools – return simple structured results; SDK will produce MCP-compliant content
@mcp.tool()
def getCompanies(limit: int = DEFAULT_LIST_LIMIT, offset: int = 0) -> list[dict]:
    lim = max(1, min(MAX_LIST_LIMIT, int(limit)))
    off = max(0, int(offset))
    return companies.iloc[off: off + lim].to_dict(orient="records")

@mcp.tool()
def getFinancials(company_id: str) -> dict:
    df = financials[financials["company_id"] == company_id]
    return {"company_id": company_id, "financials": df.to_dict(orient="records")}

@mcp.tool()
def getExposure(company_id: str) -> dict:
    df = exposure[exposure["company_id"] == company_id]
    return {"company_id": company_id, "exposure": df.to_dict(orient="records")}

@mcp.tool()
def getCovenants(company_id: str) -> dict:
    df = covenants[covenants["company_id"] == company_id]
    return {"company_id": company_id, "covenants": df.to_dict(orient="records")}

@mcp.tool()
def getEws(company_id: str) -> dict:
    df = ews[ews["company_id"] == company_id]
    return {"company_id": company_id, "ews": df.to_dict(orient="records")}

@mcp.tool()
def generateReport(company_id: str, format: str = "pdf") -> dict:
    # Agent ID is optional here; if you enforce, add header parsing via context later
    resp = generate_report_internal(
        company_id=company_id,
        x_agent_id="copilot",
        companies=companies,
        financials=financials,
        exposure=exposure,
        covenants=covenants,
        ews=ews
    )
    return {
        "company_id": company_id,
        "word_path": resp.get("word_path"),
        "pdf_path": resp.get("pdf_path"),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "format": format
    }

# Mount the MCP Streamable HTTP ASGI sub-app under /mcp
app.mount("/mcp", mcp.streamable_http_app())

# TEMP: route dump to verify /mcp appears in logs
for r in app.routes:
    try:
        logger.info("ROUTE MOUNTED: %s", getattr(r, "path", r))
    except Exception:
        pass

# Compat: redirect trailing-slash to /mcp (preserve POST body)
@app.post("/mcp/")
async def mcp_trailing_slash_compat():
    return RedirectResponse(url="/mcp", status_code=307)

# Optional: redirect legacy root POSTs to /mcp so clients that post to '/' still work
@app.post("/")
async def legacy_root_redirect():
    return RedirectResponse(url="/mcp", status_code=307)

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
