# Prompt: Quick Risk Snapshot (workIQ: quick_review)
Context:
- Company: {company_name}
- Last financial year: {last_year}
- Data sources: financials, exposure, covenants, ews (MCP)
- Use the latest financials and last 12 months of EWS

Instructions:
1. Retrieve financials, exposure, covenants, and EWS through MCP resources.
2. Compute risk_score using internal rules.
3. Output a concise 5-line summary:
    - 1 line: Risk rating (Low/Medium/High) and numeric score
    - 2 lines: Top two quantitative issues (e.g., EBITDA vs covenant, utilization)
    - 1 line: Top qualitative alert (e.g., high severity EWS)
    - 1 line: Suggested immediate action (e.g., escalate, monitor, request covenant waiver)

Output format:
RATING: {Low/Medium/High} (score: {0.00})
TOP_ISSUES:
- {issue1}
- {issue2}
ALERT: {ews_summary}
ACTION: {one_line_action}

---

# Prompt: Detailed Risk Review (workIQ: detailed_review)
Context:
- Company: {company_name}
- Use the preferred layout learned by Work IQ (appendix with raw tables)
- Provide in Word; include inline bulleted highlights and an appendix with raw numeric tables

Instructions:
1. Retrieve last 3 years financials, current exposure, covenant thresholds & ews events via MCP.
2. Compute
    - EBITDA trend (YoY)
    - Utilization %
    - Covenant compliance table (pass/fail per covenant)
    - EWS timeline
    - Risk score and rating
3. Provide:
    - Executive Summary (1 paragraph)
    - Risk Rating & score
    - Key highlights (bullet list) - these will be used as RAG highlights in the Word report
    - Suggested remediation steps (3 bullets, prioritized)
    - Appendix: Tables (financials, covenants, exposure), with source citation ("Financials: MCP resource /resource/financials/{company_id}")

Output format: Produce a JSON-like section at the start for programmatic parsing:
{
    "company": "{company_name}",
    "risk_score": {numeric},
    "risk_rating": "{Low/Medium/High}",
    "highlights": ["...","..."]
}
Followed by the natural language report.

Note: If risk_rating is High, call tool generateReport and then escalateAlert as needed.