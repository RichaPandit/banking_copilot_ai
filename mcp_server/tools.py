from docx import Document
from docx2pdf import convert
from fastapi import APIRouter, Header, HTTPException
from rag_logic.rag_highlights import generate_rag_highlights
from rag_logic.risk_scoring import compute_risk_score
import pandas as pd
import datetime
import os
from typing import Dict

router = APIRouter()

# ----------------------------------------------
# Word Report Generation
# ----------------------------------------------
def create_word_report(company_name, financials, exposure, covenants, ews, risk_score, risk_rating, rag_highlights):
    doc = Document()
    doc.add_heading(f"{company_name} - Quaterly Risk Review", level=0)

    # Financial Summary
    doc.add_heading("Financial Summary:", level=1)
    latest_fin = financials.iloc[-1]
    doc.add_paragraph(f"Revenue: {latest_fin['revenue']}")
    doc.add_paragraph(f"EBITDA: {latest_fin['ebitda']}")
    doc.add_paragraph(f"NET Income: {latest_fin['net_income']}")

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
    pdf_path = report_path.replace(".docx", ".pdf")
    convert(report_path, pdf_path)

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

# Report generation entrypoint
@router.post("/tools/generate-report/{company_id}", response_model=None)
def generate_report(company_id: str, x_agent_id: str = Header(None)):
    return {"message": "Use /tools/generate-report entrypoint in main.py for full report generation"}

# Escalate alert tool
@router.post("/tools/escalate-alert/{company_id}")
def escalate_alert(company_id: str, x_agent_id: str = Header(None)):
    # Placeholder: simulate alert
    return {"status": "alert_escalated", "company_id": company_id} 