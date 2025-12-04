from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

from mcp_server.utils import load_csv, validate_agent_id
from mcp_server.tools import router as tools_router, generate_report_internal

app = FastAPI(
    title="Banking MCP Server",
    description="MCP Server for Banking Risk Intelligence Agent (Finance + RAG + PDF/Word Reports)",
    version="1.0"
)

# ----------------------------------------------
# Allow local dev, Postman, Copilot, PowerApps, etc
# -----------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ----------------------------------------------
# Load all CSV data once (global dataframes)
# -----------------------------------------------
companies = load_csv("data/companies.csv")
financials = load_csv("data/financials.csv")
exposure = load_csv("data/exposure.csv")
covenants = load_csv("data/covenants.csv")
ews = load_csv("data/ews.csv")

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
    
# ----------------------------------------------
# Mount /tools endpoints
# -----------------------------------------------
@app.post("/tools/generate-report/{company_id}", response_model=None)
def generate_report_entry(company_id: str, x_agent_id: str = Header(None)):

    validate_agent_id(x_agent_id)

    from mcp_server.tools import generate_report

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

app.include_router(tools_router)