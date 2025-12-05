from fastapi import Request, HTTPException, FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from pydantic import BaseModel
import pandas as pd
import json
import logging
from datetime import datetime
from typing import Optional
from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal
from starlette.middleware.base import BaseHTTPMiddleware

JSONRPC_VERSION = "2.0"
PROTOCOL_VERSION = "2024-11-05"  # example protocol tag Copilot Studio understands

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
        logger.info("REQ %s %s | x-agent-id=%s x_agent_id=%s",
                    request.method, request.url.path,
                    request.headers.get("x-agent-id"),
                    request.headers.get("x_agent_id"))
        response = await call_next(request)
        logger.info("RESP %s %s | status=%s", request.method, request.url.path, response.status_code)
        return response

# ----------------------------------------------
# 1) Allow local dev, Postman, Copilot, PowerApps, etc
# -----------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# 2) Add logging last (will be outer layer; runs first on requests)
app.add_middleware(RequestLogMiddleware)

# ----------------------------------------------
# Load all CSV data once (global dataframes)
# -----------------------------------------------
companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure = load_csv("data/exposure.csv")
covenants = load_csv("data/covenants.csv")
ews = load_csv("data/ews.csv")

def jsonrpc_result(req_id, result):
    return {"jsonrpc": JSONRPC_VERSION, "id": str(req_id), "result": result}

def jsonrpc_error(req_id, code, message, data=None):
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": JSONRPC_VERSION, "id": str(req_id) if req_id is not None else None, "error": err}

def get_agent_id_from_headers(x_agent_id: Optional[str], x_agent_id_alt: Optional[str]):
    agent_id = x_agent_id or x_agent_id_alt
    if not agent_id:
        raise HTTPException(status_code=401, detail="Missing API key header (x_agent_id or x-agent-id)")
    validate_agent_id(agent_id)
    return agent_id

# --- tool definitions exposed via MCP ---
def mcp_tools_list():
    return {
        "tools": [
            {
                "name": "getCompanies",
                "description": "Return borrowers: company_id, company_name, sector.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "limit": {"type": "integer", "minimum": 1, "maximum": 200},
                        "offset": {"type": "integer", "minimum": 0}
                    },
                    "additionalProperties": False
                },
                "outputSchema": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "company_id": {"type": "string"},
                            "company_name": {"type": "string"},
                            "sector": {"type": "string"}
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
                "outputSchema": {"type": "object"}  # tailor to your payload
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
                        "format": {"type": "string", "enum": ["word", "pdf"]}  # enums are treated as strings by Studio
                    },
                    "required": ["company_id"],
                    "additionalProperties": False
                },
                "outputSchema": {
                    "type": "object",
                    "properties": {
                        "word_path": {"type": "string"},
                        "pdf_path": {"type": "string"},
                        "created_at": {"type": "string", "format": "date-time"}
                    }
                }
            }
        ]
    }

async def mcp_tools_dispatch(name: str, args: dict, agent_id: str):
    # Simple router
    if name == "getCompanies":
        # page/limit to keep payloads < 500KB for Studio connector pipeline
        limit = int(args.get("limit", 50))
        offset = int(args.get("offset", 0))
        rows = companies.iloc[offset: offset + min(limit, 200)]
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
        # Call your internal report generator
        resp = generate_report_internal(
            company_id=company_id,
            x_agent_id=agent_id,
            companies=companies,
            financials=financials,
            exposure=exposure,
            covenants=covenants,
            ews=ews
        )
        # Ensure a stable shape
        return {
            "company_id": company_id,
            "word_path": resp.get("word_path"),
            "pdf_path": resp.get("pdf_path"),
            "created_at": datetime.utcnow().isoformat() + "Z",
            "format": fmt
        }

    raise ValueError(f"Unknown tool: {name}")

def _require(d: dict, key: str) -> str:
    v = d.get(key)
    if not v:
        raise ValueError(f"Missing required argument '{key}'")
    return v

# ----------------------------------------------
# MCP SOURCE ENDPOINTS
# -----------------------------------------------
@app.get("/resources/companies")
def get_companies(x_agent_id: str = Header(None)):
    validate_agent_id(x_agent_id)
    return companies.to_dict(orient="records")

@app.get("/resources/financials/{company_id}")
def get_financials(company_id: str, x_agent_id: str = Header(None)):
    validate_agent_id(x_agent_id)
    data = financials[financials["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/exposure/{company_id}")
def get_exposure(company_id: str, x_agent_id: str = Header(None)):
    validate_agent_id(x_agent_id)
    data = exposure[exposure["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/covenants/{company_id}")
def get_covenants(company_id: str, x_agent_id: str = Header(None)):
    validate_agent_id(x_agent_id)
    data = covenants[covenants["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/ews/{company_id}")
def get_ews(company_id: str, x_agent_id: str = Header(None)):
    validate_agent_id(x_agent_id)
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/debug/headers")
async def debug_headers(request: Request):
    headers = dict(request.headers)
    return {
        "x-agent-id": headers.get("x-agent-id"),
        "x_agent_id": headers.get("x_agent_id"),
        "user-agent": headers.get("user-agent"),
        "content-type": headers.get("content-type")
    }

# ----------------------------------------------
# Mount /tools endpoints
# -----------------------------------------------
@app.post("/tools/generate-report/{company_id}", response_model=None)
def generate_report_entry(company_id: str, x_agent_id: str = Header(None), x_agent_id_alt: Optional[str] = Header(None, alias="x-agent-id")):

    # Accept both header spellings; validate
    agent_id = x_agent_id or x_agent_id_alt
    validate_agent_id(agent_id)

    return generate_report_internal(
        company_id=company_id,
        x_agent_id=x_agent_id,
        companies=companies,
        financials=financials,
        exposure=exposure,
        covenants=covenants,
        ews=ews
    )
    
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/mcp/openapi")
def mcp_openapi():
    """
    Return OpenAPI describing /resources/* and /tools/*.
    Minimal spec is fine; Studio can parse operations/params.
    """
    return {
      "openapi": "3.0.1",
      "info": {"title": "Banking MCP Server", "version": "1.0"},
      "paths": {
        "/resources/companies": {"get": {"summary": "Companies", "responses": {"200": {"description": "OK"}}}},
        "/resources/financials/{company_id}": {"get": {"parameters": [{"name": "company_id","in": "path","required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
        "/resources/exposure/{company_id}":  {"get": {"parameters": [{"name": "company_id","in": "path","required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
        "/resources/covenants/{company_id}": {"get": {"parameters": [{"name": "company_id","in": "path","required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
        "/resources/ews/{company_id}":       {"get": {"parameters": [{"name": "company_id","in": "path","required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}},
        "/tools/generate-report/{company_id}": {"post": {"parameters": [{"name": "company_id","in": "path","required": True, "schema": {"type": "string"}}], "responses": {"200": {"description": "OK"}}}}
      }
    }

@app.post("/mcp")
async def mcp_endpoint(request: Request, x_agent_id: Optional[str] = Header(None), x_agent_id_alt: Optional[str] = Header(None, alias="x-agent-id")):
    """
    Streamable HTTP style: Copilot Studio sends discrete JSON-RPC 2.0 POSTs.
    We return a single JSON-RPC response per call.
    """
    
    headers = dict(request.headers)
    print("HEADERS:", headers.get("x-agent-id"), headers.get("x_agent_id"))

    try:
        payload = await request.json()
    except Exception:
        return jsonrpc_error(None, -32700, "Parse error")

    # Support batch? Copilot Studio uses single calls here; handle object only
    if not isinstance(payload, dict):
        return jsonrpc_error(None, -32600, "Invalid Request (expected object)")

    req_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {}) or {}

    # Validate auth (API key header)
    try:
        agent_id = get_agent_id_from_headers(x_agent_id, x_agent_id_alt)
    except HTTPException as ex:
        return jsonrpc_error(req_id, -32001, f"Unauthorized: {ex.detail}")

    # Route by method
    if method == "initialize":
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "tools": {"listChanged": True}
                # optional: "logging": {}, "prompts": {"listChanged": True}, "resources": {"listChanged": True}
            },
            "serverInfo": {"name": "BankingMCP", "version": "1.0.0"}
        }
        return jsonrpc_result(req_id, result)

    if method == "notifications/initialized":
        # No response body is required by JSON-RPC; return success ack
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
        except Exception as e:
            # Avoid leaking internals; log e server-side
            return jsonrpc_error(req_id, -32000, "Server error")

    # Unknown method
    return jsonrpc_error(req_id, -32601, f"Method not found: {method}")


app.include_router(tools_router)