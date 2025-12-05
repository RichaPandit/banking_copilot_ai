from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Optional, Dict, Any
import logging
import json
import pandas as pd
from datetime import datetime

# Import mcp_server tools
from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------
JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"  # Protocol tag Copilot Studio understands
AGENT_HEADER: str = "x-agent-key"     # Hyphenated header to avoid proxy stripping
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50

# ------------------------------------------------------------------
# FastAPI app and logging
# ------------------------------------------------------------------
app = FastAPI(
    title="Banking MCP Server",
    description="MCP Server for Banking Risk Intelligence Agent (Finance + RAG + PDF/Word Reports)",
    version="1.0"
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # Log method, path, and target headers
        logger.info(
            "REQ %s %s | %s=%s %s=%s",
            request.method,
            request.url.path,
            AGENT_HEADER,
            request.headers.get(AGENT_HEADER),
            AGENT_HEADER.replace('-', '_'),
            request.headers.get(AGENT_HEADER.replace('-', '_')),
        )
        response = await call_next(request)
        logger.info("RESP %s %s | status=%s", request.method, request.url.path, response.status_code)
        return response

# CORS (inner) then logging (outer)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.add_middleware(RequestLogMiddleware)

# ----------------------------------------------
# Load all CSV data once (global dataframes)
# -----------------------------------------------
companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure = load_csv("data/exposure.csv")
covenants = load_csv("data/covenants.csv")
ews = load_csv("data/ews.csv")

def jsonrpc_result(req_id: Optional[str], result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": str(req_id), "result": result}

def jsonrpc_error(req_id: Optional[str], code: int, message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": JSONRPC_VERSION, "id": (str(req_id) if req_id is not None else None), "error": err}


# ------------------------------------------------------------------
# Utility: resolve and validate agent header
# ------------------------------------------------------------------
def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)  # Enforces prefix like `agent-`
    return agent_id

# ------------------------------------------------------------------
# MCP tool definitions
# ------------------------------------------------------------------
def mcp_tools_list() -> Dict[str, Any]:
    return {
        "tools": [
            {
                "name": "getCompanies",
                "description": "Return borrowers: company_id, company_name, sector.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit":  {"type": "integer", "minimum": 1, "maximum": MAX_LIST_LIMIT},
                        "offset": {"type": "integer", "minimum": 0}
                    },
                    "additionalProperties": False
                },
                "outputSchema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company_id":   {"type": "string"},
                            "company_name": {"type": "string"},
                            "sector":       {"type": "string"}
                        },
                        "required": ["company_id", "company_name"]
                    }
                }
            },
            {
                "name": "getFinancials",
                "description": "Return income statement & balance sheet time series for a company.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"company_id": {"type": "string"}},
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {"type": "object"}
            },
            {
                "name": "getExposure",
                "description": "Return sanctioned limit, utilized amount, overdue, collateral, DPD.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"company_id": {"type": "string"}},
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {"type": "object"}
            },
            {
                "name": "getCovenants",
                "description": "Return covenant thresholds and last actuals.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"company_id": {"type": "string"}},
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {"type": "object"}
            },
            {
                "name": "getEws",
                "description": "Return early warning signal events.",
                "inputSchema": {
                    "type": "object",
                    "properties": {"company_id": {"type": "string"}},
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {"type": "object"}
            },
            {
                "name": "generateReport",
                "description": "Create a Word/PDF risk review report; return file paths + metadata.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "company_id": {"type": "string"},
                        "format": {"type": "string", "enum": ["word", "pdf"]}
                    },
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {
                    "type": "object",
                    "properties": {
                        "word_path":  {"type": "string"},
                        "pdf_path":   {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"}
                    }
                }
            }
        ]
    }

# ------------------------------------------------------------------
# MCP tool dispatcher
# ------------------------------------------------------------------
def _require(d: Dict[str, Any], key: str) -> str:
    v = d.get(key)
    if not v:
        raise ValueError(f"Missing required argument '{key}'")
    return v

async def mcp_tools_dispatch(name: str, args: Dict[str, Any], agent_id: str) -> Any:
    if name == "getCompanies":
        limit = int(args.get("limit", DEFAULT_LIST_LIMIT))
        offset = int(args.get("offset", 0))
        limit = min(max(limit, 1), MAX_LIST_LIMIT)
        rows = companies.iloc[offset: offset + limit]
        return rows.to_dict(orient="records")

    if name == "getFinancials":
        company_id = _require(args, "company_id")
        df = financials[financials["company_id"] == company_id]
        return {"company_id": company_id, "financials": df.to_dict(orient="records")}

    if name == "getExposure":
        company_id = _require(args, "company_id")
        df = exposure[exposure["company_id"] == company_id]
        return {"company_id": company_id, "exposure": df.to_dict(orient="records")}

    if name == "getCovenants":
        company_id = _require(args, "company_id")
        df = covenants[covenants["company_id"] == company_id]
        return {"company_id": company_id, "covenants": df.to_dict(orient="records")}

    if name == "getEws":
        company_id = _require(args, "company_id")
        df = ews[ews["company_id"] == company_id]
        return {"company_id": company_id, "ews": df.to_dict(orient="records")}

    if name == "generateReport":
        company_id = _require(args, "company_id")
        fmt = args.get("format", "pdf")
        resp = generate_report_internal(
            company_id=company_id,
            x_agent_id=agent_id,
            companies=companies,
            financials=financials,
            exposure=exposure,
            covenants=covenants,
            ews=ews
        )
        return {
            "company_id": company_id,
            "word_path":  resp.get("word_path"),
            "pdf_path":   resp.get("pdf_path"),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "format": fmt
        }

    raise ValueError(f"Unknown tool: {name}")

# ----------------------------------------------
# MCP SOURCE ENDPOINTS (protected by x-agent-key)
# -----------------------------------------------
@app.get("/resources/companies")
def get_companies_endpoint(
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
    limit: int = DEFAULT_LIST_LIMIT,
    offset: int = 0
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    # Limit response size to avoid Studio connector failures
    limit = min(max(limit, 1), MAX_LIST_LIMIT)
    rows = companies.iloc[offset: offset + limit]
    return rows.to_dict(orient="records")


@app.get("/resources/financials/{company_id}")
def get_financials_endpoint(
    company_id: str,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = financials[financials["company_id"] == company_id]
    return data.to_dict(orient="records")


@app.get("/resources/exposure/{company_id}")
def get_exposure_endpoint(
    company_id: str,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = exposure[exposure["company_id"] == company_id]
    return data.to_dict(orient="records")


@app.get("/resources/covenants/{company_id}")
def get_covenants_endpoint(
    company_id: str,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = covenants[covenants["company_id"] == company_id]
    return data.to_dict(orient="records")


@app.get("/resources/ews/{company_id}")
def get_ews_endpoint(
    company_id: str,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

# ----------------------------------------------
# Mount /tools endpoints
# -----------------------------------------------
@app.post("/tools/generate-report/{company_id}")
def generate_report_entry(
    company_id: str,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    return generate_report_internal(
        company_id=company_id,
        x_agent_id=agent_id,
        companies=companies,
        financials=financials,
        exposure=exposure,
        covenants=covenants,
        ews=ews
    )

# ------------------------------------------------------------------
# Health/debug
# ------------------------------------------------------------------    
@app.get("/health")
def health():
    logger.info("HEALTH CHECK HIT")
    return {"status": "ok"}


@app.get("/debug/headers")
async def debug_headers(request: Request):
    headers = dict(request.headers)
    return {
        AGENT_HEADER: headers.get(AGENT_HEADER),
        AGENT_HEADER.replace('-', '_'): headers.get(AGENT_HEADER.replace('-', '_')),
        "user-agent": headers.get("user-agent"),
        "content-type": headers.get("content-type"),
    }

# ------------------------------------------------------------------
# MCP JSON-RPC endpoint (Streamable HTTP style)
# ------------------------------------------------------------------
@app.post("/mcp")
async def mcp_endpoint(
    request: Request,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    # Resolve & validate auth first
    try:
        agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    except HTTPException as ex:
        # We still want to parse JSON to echo the id if possible
        try:
            payload = await request.json()
            req_id = payload.get("id")
        except Exception:
            req_id = None
        return jsonrpc_error(req_id, -32001, f"Unauthorized: {ex.detail}")

    # Parse JSON-RPC
    try:
        payload = await request.json()
    except Exception:
        return jsonrpc_error(None, -32700, "Parse error")

    if not isinstance(payload, dict):
        return jsonrpc_error(None, -32600, "Invalid Request (expected object)")

    req_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {}) or {}

    if method == "initialize":
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {"tools": {"listChanged": True}},
            "serverInfo": {"name": "BankingMCP", "version": "1.0.0"}
        }
        return jsonrpc_result(req_id, result)

    if method == "notifications/initialized":
        return jsonrpc_result(req_id, {"ok": True})

    if method == "tools/list":
        return jsonrpc_result(req_id, mcp_tools_list())

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments") or {}
        try:
            result = await mcp_tools_dispatch(name, arguments, agent_id)
            return jsonrpc_result(req_id, {"content": result})
        except ValueError as ve:
            return jsonrpc_error(req_id, -32602, f"Invalid params: {ve}")
        except Exception:
            return jsonrpc_error(req_id, -32000, "Server error")

    return jsonrpc_error(req_id, -32601, f"Method not found: {method}")

# --- NEW: Root handlers so onboarding probe passes ---
@app.get("/")
def root_probe():
    """Return 200 OK to allow connector wizard to proceed."""
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp"}

@app.post("/")
async def root_passthrough(
    request: Request,
    x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER),
    x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')),
):
    """If the client posts JSON-RPC to '/', forward to /mcp when auth is present; else return 200 info."""
    if x_agent_key or x_agent_key_alt:
        return await mcp_endpoint(request, x_agent_key=x_agent_key, x_agent_key_alt=x_agent_key_alt)
    # No auth header: respond 200 with guidance so probe succeeds
    try:
        _ = await request.json()
        return {"message": "Use POST /mcp with API key header.", "mcpEntry": "/mcp"}
    except Exception:
        return {"message": "Root accepts GET 200; use POST /mcp for MCP."}

# OpenAPI preview endpoint
@app.get("/mcp/openapi")
def mcp_openapi():
    return {
        "openapi": "3.0.1",
        "info": {"title": "Banking MCP Server", "version": "1.0"},
        "paths": {
            "/resources/companies": {"get": {"summary": "Companies", "responses": {"200": {"description": "OK"}}}},
            "/resources/financials/{company_id}": {"get": {"parameters": [{"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
            "/resources/exposure/{company_id}":  {"get": {"parameters": [{"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
            "/resources/covenants/{company_id}": {"get": {"parameters": [{"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
            "/resources/ews/{company_id}":       {"get": {"parameters": [{"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
            "/tools/generate-report/{company_id}": {"post": {"parameters": [{"name": "company_id", "in": "path", "required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}}
        }
    }

app.include_router(tools_router)