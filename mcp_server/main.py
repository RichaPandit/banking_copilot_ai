
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response, RedirectResponse
from typing import Optional, Dict, Any
import logging, json
from datetime import datetime
import pandas as pd

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal

JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"
AGENT_HEADER: str = "x-agent-key"
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50

app = FastAPI(title="Banking MCP Server", description="MCP Server for Banking Risk Intelligence Agent", version="1.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info("REQ %s %s | %s=%s %s=%s", request.method, request.url.path,
                    AGENT_HEADER, request.headers.get(AGENT_HEADER),
                    AGENT_HEADER.replace('-', '_'), request.headers.get(AGENT_HEADER.replace('-', '_')))
        response = await call_next(request)
        logger.info("RESP %s %s | status=%s", request.method, request.url.path, response.status_code)
        return response

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.add_middleware(RequestLogMiddleware)

companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure   = load_csv("data/exposure.csv")
covenants  = load_csv("data/covenants.csv")
ews        = load_csv("data/ews.csv")

def jsonrpc_result(req_id: Optional[str], result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": (str(req_id) if req_id is not None else None), "result": result}

def jsonrpc_error(req_id: Optional[str], code: int, message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": JSONRPC_VERSION, "id": (str(req_id) if req_id is not None else None), "error": err}

def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)
    return agent_id

def mcp_tools_list() -> Dict[str, Any]:
    return {
        "tools": [
            {"name": "getCompanies", "description": "Return borrowers: company_id, company_name, sector.",
             "inputSchema": {"type": "object", "properties": {"limit": {"type": "integer", "minimum": 1, "maximum": MAX_LIST_LIMIT}, "offset": {"type": "integer", "minimum": 0}}, "additionalProperties": False},
             "outputSchema": {"type": "array", "items": {"type": "object", "properties": {"company_id": {"type": "string"}, "company_name": {"type": "string"}, "sector": {"type": "string"}}, "required": ["company_id", "company_name"]}}},
            {"name": "getFinancials", "description": "Return time series for a company.",
             "inputSchema": {"type": "object", "properties": {"company_id": {"type": "string"}}, "required": ["company_id"], "additionalProperties": False},
             "outputSchema": {"type": "object"}},
            {"name": "getExposure",   "description": "Return sanctioned limit, utilized amount, overdue, collateral, DPD.",
             "inputSchema": {"type": "object", "properties": {"company_id": {"type": "string"}}, "required": ["company_id"], "additionalProperties": False},
             "outputSchema": {"type": "object"}},
            {"name": "getCovenants",  "description": "Return covenant thresholds and last actuals.",
             "inputSchema": {"type": "object", "properties": {"company_id": {"type": "string"}}, "required": ["company_id"], "additionalProperties": False},
             "outputSchema": {"type": "object"}},
            {"name": "getEws",        "description": "Return early warning signal events.",
             "inputSchema": {"type": "object", "properties": {"company_id": {"type": "string"}}, "required": ["company_id"], "additionalProperties": False},
             "outputSchema": {"type": "object"}},
            {"name": "generateReport", "description": "Create a Word/PDF risk review report; return file paths + metadata.",
             "inputSchema": {"type": "object", "properties": {"company_id": {"type": "string"}, "format": {"type": "string", "enum": ["word", "pdf"]}}, "required": ["company_id"], "additionalProperties": False},
             "outputSchema": {"type": "object", "properties": {"word_path": {"type": "string"}, "pdf_path": {"type": "string"}, "created_at": {"type": "string", "format": "date-time"}}}}
        ]
    }

async def _dispatch_tool(name: str, args: Dict[str, Any], agent_id: str) -> Any:
    if name == "getCompanies":
        limit = int(args.get("limit", DEFAULT_LIST_LIMIT)); offset = int(args.get("offset", 0))
        limit = min(max(limit, 1), MAX_LIST_LIMIT)
        return companies.iloc[offset: offset + limit].to_dict(orient="records")
    if name == "getFinancials":
        cid = args.get("company_id");
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = financials[financials["company_id"] == cid]
        return {"company_id": cid, "financials": df.to_dict(orient="records")}
    if name == "getExposure":
        cid = args.get("company_id");
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = exposure[exposure["company_id"] == cid]
        return {"company_id": cid, "exposure": df.to_dict(orient="records")}
    if name == "getCovenants":
        cid = args.get("company_id");
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = covenants[covenants["company_id"] == cid]
        return {"company_id": cid, "covenants": df.to_dict(orient="records")}
    if name == "getEws":
        cid = args.get("company_id");
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = ews[ews["company_id"] == cid]
        return {"company_id": cid, "ews": df.to_dict(orient="records")}
    if name == "generateReport":
        cid = args.get("company_id");
        if not cid: raise ValueError("Missing required argument 'company_id'")
        resp = generate_report_internal(company_id=cid, x_agent_id=agent_id, companies=companies, financials=financials, exposure=exposure, covenants=covenants, ews=ews)
        return {"company_id": cid, "word_path": resp.get("word_path"), "pdf_path": resp.get("pdf_path"), "created_at": datetime.utcnow().isoformat() + "Z", "format": args.get("format", "pdf")}
    raise ValueError(f"Unknown tool: {name}")

async def process_mcp(payload: Dict[str, Any], x_agent_key: Optional[str], x_agent_key_alt: Optional[str], allow_unauth_discovery: bool = True) -> Response:
    if not isinstance(payload, dict):
        return Response(content=json.dumps(jsonrpc_error(None, -32600, "Invalid Request (expected object)")), media_type="application/json")

    req_id = payload.get("id"); method = payload.get("method"); params = payload.get("params", {}) or {}

    # Notifications MUST NOT send a response body per JSON-RPC 2.0
    if method == "notifications/initialized":
        return Response(status_code=204)

    discovery_methods = {"initialize", "tools/list"}
    if method in discovery_methods and allow_unauth_discovery:
        agent_id = x_agent_key or x_agent_key_alt or "agent-probe"
    else:
        try:
            agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
        except HTTPException as ex:
            return Response(content=json.dumps(jsonrpc_error(req_id, -32001, f"Unauthorized: {ex.detail}")), media_type="application/json")

    if method == "initialize":
        result = {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {
                "logging": {}, "completions": {}, "tools": {"listChanged": True}, "prompts": {"listChanged": True}, "resources": {"listChanged": True}
            },
            "serverInfo": {"name": "BankingMCP", "version": "1.0.0"}
        }
        return Response(content=json.dumps(jsonrpc_result(req_id, result)), media_type="application/json")

    if method == "tools/list":
        return Response(content=json.dumps(jsonrpc_result(req_id, mcp_tools_list())), media_type="application/json")

    if method == "tools/call":
        name = params.get("name"); arguments = params.get("arguments") or {}
        try:
            content = await _dispatch_tool(name, arguments, agent_id)
            return Response(content=json.dumps(jsonrpc_result(req_id, {"content": content})), media_type="application/json")
        except ValueError as ve:
            return Response(content=json.dumps(jsonrpc_error(req_id, -32602, f"Invalid params: {ve}")), media_type="application/json")
        except Exception:
            return Response(content=json.dumps(jsonrpc_error(req_id, -32000, "Server error")), media_type="application/json")

    return Response(content=json.dumps(jsonrpc_error(req_id, -32601, f"Method not found: {method}")), media_type="application/json")

# REST endpoints
@app.get("/resources/companies")
def get_companies_endpoint(x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_')), limit: int = DEFAULT_LIST_LIMIT, offset: int = 0):
    resolve_agent_id(x_agent_key, x_agent_key_alt)
    limit = min(max(limit, 1), MAX_LIST_LIMIT)
    return companies.iloc[offset: offset + limit].to_dict(orient="records")

@app.get("/resources/financials/{company_id}")
def get_financials_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = financials[financials["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/exposure/{company_id}")
def get_exposure_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = exposure[exposure["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/covenants/{company_id}")
def get_covenants_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = covenants[covenants["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/ews/{company_id}")
def get_ews_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.post("/tools/generate-report/{company_id}")
def generate_report_entry(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    return generate_report_internal(company_id=company_id, x_agent_id=agent_id, companies=companies, financials=financials, exposure=exposure, covenants=covenants, ews=ews)

@app.get("/health")
def health():
    return {"status": "ok", "variant": "patched6"}

@app.get("/")
def root_probe():
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp", "variant": "patched6"}

# --- 307 redirect from POST / to POST /mcp (forces wizard to use canonical endpoint) ---
@app.post("/")
async def root_redirect():
    return RedirectResponse(url="/mcp", status_code=307)

@app.post("/mcp")
async def mcp_endpoint(request: Request, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER.replace('-', '_'))):
    try:
        payload = await request.json()
    except Exception:
        return jsonrpc_error(None, -32700, "Parse error")
    if isinstance(payload, dict) and payload.get("method") == "notifications/initialized":
        return Response(status_code=204)
    return await process_mcp(payload, x_agent_key, x_agent_key_alt, allow_unauth_discovery=True)

app.include_router(tools_router)