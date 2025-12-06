from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import Response
from typing import Optional, Dict, Any, List
import logging, json, os
from datetime import datetime
import pandas as pd

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal

JSONRPC_VERSION: str = "2.0"
PROTOCOL_VERSION: str = "2024-11-05"
AGENT_HEADER: str = "x-agent-key"
AGENT_HEADER_ALT: str = AGENT_HEADER.replace('-', '_')
MAX_LIST_LIMIT: int = 200
DEFAULT_LIST_LIMIT: int = 50
DEV_ASSUME_KEY: Optional[str] = os.getenv("MCP_DEV_ASSUME_KEY")

app = FastAPI(title="Banking MCP Server", description="MCP Server for Banking Risk Intelligence Agent", version="1.0")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger("banking-mcp")

class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        logger.info("REQ %s %s | %s=%s %s=%s", request.method, request.url.path,
                    AGENT_HEADER, request.headers.get(AGENT_HEADER),
                    AGENT_HEADER_ALT, request.headers.get(AGENT_HEADER_ALT))
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

def jsonrpc_result(req_id: Any, result: Dict[str, Any]) -> Dict[str, Any]:
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "result": result}

def jsonrpc_error(req_id: Any, code: int, message: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    err = {"code": code, "message": message}
    if data is not None:
        err["data"] = data
    return {"jsonrpc": JSONRPC_VERSION, "id": req_id, "error": err}

# --- Missing helpers now added ---

def resolve_agent_id(primary: Optional[str], alternate: Optional[str]) -> str:
    """Resolve and validate the agent id from headers; raise 401 if missing/invalid."""
    agent_id = primary or alternate
    if not agent_id:
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    validate_agent_id(agent_id)
    return agent_id

def mcp_tools_list() -> Dict[str, Any]:
    """Return a Studio-friendly list of tools (no $ref, strict schemas)."""
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
                "description": "Return time series for a company.",
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

async def _dispatch_tool(name: str, args: Dict[str, Any], agent_id: str) -> Any:
    if name == "getCompanies":
        limit = int(args.get("limit", DEFAULT_LIST_LIMIT))
        offset = int(args.get("offset", 0))
        limit = min(max(limit, 1), MAX_LIST_LIMIT)
        return companies.iloc[offset: offset + limit].to_dict(orient="records")
    
    if name == "getFinancials":
        cid = args.get("company_id")
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = financials[financials["company_id"] == cid]
        return {"company_id": cid, "financials": df.to_dict(orient="records")}
    
    if name == "getExposure":
        cid = args.get("company_id")
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = exposure[exposure["company_id"] == cid]
        return {"company_id": cid, "exposure": df.to_dict(orient="records")}
    
    if name == "getCovenants":
        cid = args.get("company_id")
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = covenants[covenants["company_id"] == cid]
        return {"company_id": cid, "covenants": df.to_dict(orient="records")}
    
    if name == "getEws":
        cid = args.get("company_id")
        if not cid: raise ValueError("Missing required argument 'company_id'")
        df = ews[ews["company_id"] == cid]
        return {"company_id": cid, "ews": df.to_dict(orient="records")}
    
    if name == "generateReport":
        cid = args.get("company_id")
        if not cid: raise ValueError("Missing required argument 'company_id'")

        resp = generate_report_internal(
            company_id=cid,
            x_agent_id=agent_id,
            companies=companies,
            financials=financials,
            exposure=exposure,
            covenants=covenants,
            ews=ews
            )
        return {"company_id": cid,
                "word_path": resp.get("word_path"),
                "pdf_path": resp.get("pdf_path"),
                "created_at": datetime.utcnow().isoformat() + "Z",
                "format": args.get("format", "pdf")
            }
    raise ValueError(f"Unknown tool: {name}")

async def process_mcp_element(payload: Dict[str, Any], x_agent_key: Optional[str], x_agent_key_alt: Optional[str], allow_unauth_discovery: bool = True) -> Optional[Dict[str, Any]]:
    req_id = payload.get("id")
    method = payload.get("method")
    params = payload.get("params", {}) or {}

    logger.info("MCP REQ: id=%s method=%s", req_id, method)

    if not method:
        return jsonrpc_error(req_id, -32600, "Invalid Request")
    
    if method.startswith("notifications/"):
        logger.info("Ignoring notification: %s", method)
        return None

    discovery_methods = {"initialize", "tools/list", "resources/list"}
    if method in discovery_methods or method.startswith("tools/"):
        agent_id = "copilot"
    else:
        fallback = os.getenv("MCP_DEV_ASSUME_KEY")
        try:
            agent_id = (x_agent_key or x_agent_key_alt or fallback)
            if not agent_id:
                raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
            validate_agent_id(agent_id)
        except HTTPException as ex:
            return jsonrpc_error(req_id, -32001, f"Unauthorized: {ex.detail}")

    if method == "initialize":
        pv = params.get("protocolVersion") or PROTOCOL_VERSION
        result = {
            "protocolVersion": pv,
            "capabilities": {
                "tools": {
                    "available": True,
                    "listChanged": True
                    },
                "resources": {
                    "available": True,
                    "listChanged": True
                    }
            },
            "serverInfo": {
                "name": "BankingMCP",
                "version": "1.0.0"
                }
        }
        return jsonrpc_result(req_id, result)

    if method == "tools/list":
        result = mcp_tools_list()
        return jsonrpc_result(req_id, result)

    if method == "resources/list":
        result = {
            "resources": []
        }
        return jsonrpc_result(req_id, result)

    if method == "tools/call":
        name = params.get("name")
        arguments = params.get("arguments", {})
        
        try:
            content = await _dispatch_tool(name, arguments, agent_id)
            return jsonrpc_result(req_id, {"toolResult": content})
        except ValueError as ve:
            return jsonrpc_error(req_id, -32602, f"Invalid params: {ve}")
        except Exception:
            return jsonrpc_error(req_id, -32000, "Server error")

    return jsonrpc_error(req_id, -32601, f"Method not found: {method}")

async def _handle_jsonrpc(request: Request, x_agent_key: Optional[str], x_agent_key_alt: Optional[str]) -> Response:
    try:
        payload = await request.json()
    except Exception:
        return Response(content=json.dumps(jsonrpc_error(None, -32700, "Parse error")), media_type="application/json")

    logger.info("RAW BODY: %s", str(payload)[:500])

    if isinstance(payload, list):
        if all((not isinstance(el, dict)) or (not el.get("method")) for el in payload):
            logger.info("Batch probe received without methods; returning empty array to satisfy client")
            return Response(content="[]", media_type="application/json")
        responses: List[Dict[str, Any]] = []
        for el in payload:
            if not isinstance(el, dict):
                responses.append(jsonrpc_error(None, -32600, "Invalid Request"))
                continue
            resp = await process_mcp_element(el, x_agent_key, x_agent_key_alt, allow_unauth_discovery=True)
            if resp is not None:
                responses.append(resp)
        return Response(content=json.dumps(responses), media_type="application/json")

    if not isinstance(payload, dict):
        return Response(content=json.dumps(jsonrpc_error(None, -32600, "Invalid Request (expected object or batch)")), media_type="application/json")

    resp = await process_mcp_element(payload, x_agent_key, x_agent_key_alt, allow_unauth_discovery=True)
    if resp is None:
        return Response(status_code=200)
    return Response(content=json.dumps(resp), media_type="application/json")

@app.post("/")
async def root_forward(request: Request, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    return await _handle_jsonrpc(request, x_agent_key, x_agent_key_alt)

@app.post("/mcp")
async def mcp_endpoint(request: Request, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    return await _handle_jsonrpc(request, x_agent_key, x_agent_key_alt)

@app.get("/health")
def health():
    return {"status": "ok", "variant": "mcp-final", "dev_assume_key": bool(DEV_ASSUME_KEY)}

@app.get("/")
def root_probe():
    return {"name": "Banking MCP Server", "status": "ready", "mcpEntry": "/mcp", "variant": "patched10a"}

# REST endpoints using resolve_agent_id
@app.get("/resources/companies")
def get_companies_endpoint(x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT), limit: int = DEFAULT_LIST_LIMIT, offset: int = 0):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    limit = min(max(limit, 1), MAX_LIST_LIMIT)
    return companies.iloc[offset: offset + limit].to_dict(orient="records")

@app.get("/resources/financials/{company_id}")
def get_financials_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = financials[financials["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/exposure/{company_id}")
def get_exposure_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = exposure[exposure["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/covenants/{company_id}")
def get_covenants_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = covenants[covenants["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.get("/resources/ews/{company_id}")
def get_ews_endpoint(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    data = ews[ews["company_id"] == company_id]
    return data.to_dict(orient="records")

@app.post("/tools/generate-report/{company_id}")
def generate_report_entry(company_id: str, x_agent_key: Optional[str] = Header(None, alias=AGENT_HEADER), x_agent_key_alt: Optional[str] = Header(None, alias=AGENT_HEADER_ALT)):
    agent_id = resolve_agent_id(x_agent_key, x_agent_key_alt)
    return generate_report_internal(company_id=company_id, x_agent_id=agent_id, companies=companies, financials=financials, exposure=exposure, covenants=covenants, ews=ews)

app.include_router(tools_router)
