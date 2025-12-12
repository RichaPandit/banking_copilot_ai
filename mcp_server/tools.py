from docx import Document
from fastapi import APIRouter, Header, HTTPException
from rag_logic.rag_highlights import generate_rag_highlights
from rag_logic.risk_scoring import compute_risk_score
import pandas as pd
import datetime
import os
from typing import Dict, Optional

router = APIRouter()


# Use a writable base path on App Service Linux
BASE_DIR = os.environ.get("APP_BASE_DIR", "/home/site/wwwroot")
REPORT_DIR = os.path.join(BASE_DIR, "reports", "generated_reports")

# ----------------------------------------------
# Word Report Generation
# ----------------------------------------------
def create_word_report(company_name, financials, exposure, covenants, ews, risk_score, risk_rating, rag_highlights):

    # Validate data presence to avoid iloc errors
    if financials.empty or exposure.empty or covenants.empty:
        raise HTTPException(status_code=400, detail="Insufficient data to generate report")
 
    # Ensure we pick the latest financials
    if "year" in financials.columns:
        financials = financials.sort_values("year")

    doc = Document()
    doc.add_heading(f"{company_name} - Quaterly Risk Review", level=0)

    # Financial Summary
    doc.add_heading("Financial Summary:", level=1)
    latest_fin = financials.iloc[-1]
    doc.add_paragraph(f"Revenue: {latest_fin['revenue']}")
    doc.add_paragraph(f"EBITDA: {latest_fin['ebitda']}")
    doc.add_paragraph(f"Net Income: {latest_fin['net_income']}")

    # Loan Exposure
    doc.add_heading("Loan Exposure:", level=1)
    exp = exposure.iloc[0]
    doc.add_paragraph(f"Sanctioned Limit: {exp['sanctioned_limit']}")
    doc.add_paragraph(f"Utilized Amount: {exp['utilized_amount']}")
    doc.add_paragraph(f"Overdue Amount: {exp['overdue_amount']}")

    # Covenant Compliance
    doc.add_heading("Covenant Compliance:", level=1)
    cov = covenants.iloc[0]
    doc.add_paragraph(f"DSCR: {cov['dscr']}")
    doc.add_paragraph(f"Interest Coverage: {cov['interest_coverage']}")
    doc.add_paragraph(f"Current Ratio: {cov['current_ratio']}")

    # Early Warning Signals
    doc.add_heading("Early Warning Signals:", level=1)
    for idx, row in ews.iterrows():
        doc.add_paragraph(f"{row['event_date']}: {row['event']}")
    
    # Risk Summary
    doc.add_heading("Risk Summary:", level=1)
    doc.add_paragraph(f"Risk Score: {risk_score:.2f}")
    doc.add_paragraph(f"Risk Rating: {risk_rating}")

    # Key Highlights (RAG)
    doc.add_heading("Key Highlights:", level=1)
    for h in rag_highlights:
        doc.add_paragraph(f"- {h}")

    # Save Word
    report_name = f"{company_name.replace(' ','_')}_Risk_Report_{datetime.date.today()}.docx"
    report_path = os.path.join("reports/generated_reports", report_name)
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    doc.save(report_path)

    # Convert to PDF
    pdf_path: Optional[str] = report_path.replace(".docx", ".pdf")
    try:
        from docx2pdf import convert  # requires Word on Windows/macOS
        convert(report_path, pdf_path)
    except Exception:
        pdf_path = None  # return DOCX-only

    return {"word": report_path, "pdf": pdf_path, "rag_highlights": rag_highlights}

def generate_report_internal(
    company_id: str,
    x_agent_id: str,
    companies: pd.DataFrame,
    financials: pd.DataFrame,
    exposure: pd.DataFrame,
    covenants: pd.DataFrame,
    ews: pd.DataFrame
) -> Dict[str, str]:
    if not x_agent_id or not x_agent_id.startswith("agent-"):
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")

    # Validate company
    company_info = companies[companies["company_id"] == company_id]
    if company_info.empty:
        raise HTTPException(status_code=404, detail="Company not found")
    company_name = company_info["company_name"].values[0]

    # Extract data
    fin = financials[financials["company_id"] == company_id]
    exp = exposure[exposure["company_id"] == company_id]
    cov = covenants[covenants["company_id"] == company_id]
    ews_events = ews[ews["company_id"] == company_id]

    # Compute risk score
    risk_score, risk_rating = compute_risk_score(fin, exp, cov, ews_events)

    # Generate reports
    rag_highlights = generate_rag_highlights(fin, cov, exp, ews_events)
    report_paths = create_word_report(company_name, fin, exp, cov, ews_events, risk_score, risk_rating, rag_highlights)

    return {
        "status": "report_generated",
        "company": company_name,
        "risk_score": risk_score,
        "risk_rating": risk_rating,
        "word_report": report_paths["word"],
        "pdf_report": report_paths["pdf"],
        "rag_highlights": report_paths["rag_highlights"]
    }

# Escalate alert tool
@router.post("/tools/escalate-alert/{company_id}")
def escalate_alert(company_id: str, x_agent_id: str = Header(None)):
    if not x_agent_id or not x_agent_id.startswith("agent-"):
        raise HTTPException(status_code=401, detail="Invalid or missing Agent ID")
    # TODO: call your Power Automate / Logic Apps flow here
    return {"status": "alert_escalated", "company_id": company_id}