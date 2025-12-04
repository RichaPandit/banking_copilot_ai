def compute_risk_score(financial, exposure, covenants, ews_events):
    ebitda_ratio = financial["ebitda"].iloc[-1] / covenants["ebitda_min_requirement"].iloc[0]
    utilization_ratio = exposure["utilized_amount"].iloc[0] / exposure["sanctioned_limit"].iloc[0]
    covenant_compliance = sum([
        1 if covenants["dscr"].iloc[0] >= 1 else 0,
        1 if covenants["interest_coverage"].iloc[0] >= 1.5 else 0,
        1 if covenants["current_ratio"].iloc[0] >= 1 else 0
    ]) / 3
    ews_severity_mapping = {"Low":0.3, "Medium":0.6, "High":1.0}
    ews_severity = max([ews_severity_mapping.get(ev, 0) for ev in ews_events["severity"]], default=0)
    risk_score = (0.4* (1-ebitda_ratio) + 0.3*utilization_ratio + 0.2*(1-covenant_compliance) + 0.1*ews_severity)

    if risk_score < 0.3:
        rating = "Low"
    elif risk_score < 0.6:
        rating = "Medium"
    else:
        rating = "High"
    return risk_score, rating