def generate_rag_highlights(financials, covenants, exposure, ews):
    highlights = []
    latest_fin = financials.iloc[-1]
    cov = covenants.iloc[0]
    exp = exposure.iloc[0]

    if latest_fin['ebitda'] < cov['ebitda_min_requirement']:
        highlights.append("EBITDA is below covenant minimum requirement.")
    if exp['utilized_amount']/exp['sanctioned_limit'] > 0.8:
        highlights.append("Loan utilization exceeds 80% of sanctioned limit.")
    high_ews = ews[ews['severity']=="High"]
    for idx, row in high_ews.iterrows():
        highlights.append(f"High severity alert: {row['event']} on {row['event_date']}")
    return highlights