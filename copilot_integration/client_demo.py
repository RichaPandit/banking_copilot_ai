import requests
import pandas as pd
from rag_logic.risk_scoring import compute_risk_score

# ---- CONFIG ----
MCP_BASE = "http://localhost:8080"
AGENT_ID = "agent-demo-001"
COMPANY_ID = "C001"

HEADERS = {"x-agent-id": AGENT_ID}

# ---- HELPER FUNCTIONS ----
def get_resource(uri):
    resp = requests.get(f"{MCP_BASE}{uri}", headers=HEADERS)
    resp.raise_for_status()
    return pd.DataFrame(resp.json())

def generate_report(company_id):
    resp = requests.post(f"{MCP_BASE}/tools/generate-report/{company_id}", headers=HEADERS)
    print(resp.status_code, resp.text)
    resp.raise_for_status()
    return resp.json()

def escalate_alert(company_id):
    resp = requests.post(f"{MCP_BASE}/tools/escalate-alert/{company_id}", headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

# ---- FLOW ----
def main():
    print(f"\n--- Fetching MCP resources for company {COMPANY_ID}")
    financials = get_resource(f"/resources/financials/{COMPANY_ID}")
    exposure = get_resource(f"/resources/exposure/{COMPANY_ID}")
    covenants = get_resource(f"/resources/covenants/{COMPANY_ID}")
    ews = get_resource(f"/resources/ews/{COMPANY_ID}")
    company_info = get_resource(f"/resources/companies")
    company_name = company_info[company_info["company_id"]==COMPANY_ID]["company_name"].values[0]

    print(f"Company: {company_name}\nFinancials:\n{financials.tail(1)}\nExposure:\n{exposure}\nCovenants:\n{covenants}\nEWS Events:\n{ews}")

    # ---- RAG + Risk Scoring ----
    risk_score, risk_rating = compute_risk_score(financials, exposure, covenants, ews)
    print(f"\n---- Compute Risk Score----\nScore: {risk_score:.2f}, Rating: {risk_rating}")

    # ---- Generate Report ----
    report_result = generate_report(COMPANY_ID)
    print(f"\nReport Generated at: {report_result['pdf_report']}")

    # ---- Escalate alert if High Risk ----
    if risk_rating == "High":
        alert_result = escalate_alert(COMPANY_ID)
        print(f"High risk alert escalated: {alert_result}")

if __name__ == "__main__":
    main()