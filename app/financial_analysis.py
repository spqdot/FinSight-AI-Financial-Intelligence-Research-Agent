def analyze_financial_health(financial_data: dict) -> dict:
    """
    Perform a rule-based financial health assessment.

    The function uses deterministic thresholds and does not
    generate or infer financial data.
    """

    analysis = {
        "profitability": "Unavailable",
        "growth": "Unavailable",
        "capital_efficiency": "Unavailable",
        "liquidity": "Unavailable",
        "leverage": "Unavailable",
        "valuation": "Unavailable",
        "cash_generation": "Unavailable",
        "risk_flags": [],
    }

    # --------------------------------------------------
    # Profitability
    # --------------------------------------------------

    profit_margin = financial_data.get("profit_margin")
    operating_margin = financial_data.get("operating_margin")

    if profit_margin is not None:
        if profit_margin >= 0.20:
            analysis["profitability"] = "Strong"
        elif profit_margin >= 0.10:
            analysis["profitability"] = "Moderate"
        else:
            analysis["profitability"] = "Weak"

    # --------------------------------------------------
    # Growth
    # --------------------------------------------------

    revenue_growth = financial_data.get("revenue_growth")
    earnings_growth = financial_data.get("earnings_growth")

    if revenue_growth is not None:
        if revenue_growth >= 0.10:
            analysis["growth"] = "Strong"
        elif revenue_growth >= 0:
            analysis["growth"] = "Moderate"
        else:
            analysis["growth"] = "Negative"

    # --------------------------------------------------
    # Capital efficiency
    # --------------------------------------------------

    roe = financial_data.get("return_on_equity")
    roa = financial_data.get("return_on_assets")

    if roe is not None:
        if roe >= 0.20:
            analysis["capital_efficiency"] = "Strong"
        elif roe >= 0.10:
            analysis["capital_efficiency"] = "Moderate"
        else:
            analysis["capital_efficiency"] = "Weak"

    # --------------------------------------------------
    # Liquidity
    # --------------------------------------------------

    current_ratio = financial_data.get("current_ratio")
    quick_ratio = financial_data.get("quick_ratio")

    if current_ratio is not None:
        if current_ratio >= 1.5:
            analysis["liquidity"] = "Strong"
        elif current_ratio >= 1.0:
            analysis["liquidity"] = "Adequate"
        else:
            analysis["liquidity"] = "Weak"
            analysis["risk_flags"].append("Low current ratio")

    # --------------------------------------------------
    # Leverage
    # --------------------------------------------------

    debt_to_equity = financial_data.get("debt_to_equity")

    if debt_to_equity is not None:
        if debt_to_equity >= 100:
            analysis["leverage"] = "High"
            analysis["risk_flags"].append("High leverage")
        elif debt_to_equity >= 50:
            analysis["leverage"] = "Moderate"
            analysis["risk_flags"].append("Moderate leverage")
        else:
            analysis["leverage"] = "Low"

    # --------------------------------------------------
    # Valuation
    # --------------------------------------------------

    pe_ratio = financial_data.get("pe_ratio")

    if pe_ratio is not None:
        if pe_ratio >= 35:
            analysis["valuation"] = "High"
            analysis["risk_flags"].append("High P/E valuation")
        elif pe_ratio >= 20:
            analysis["valuation"] = "Moderate"
        elif pe_ratio > 0:
            analysis["valuation"] = "Lower"

    # --------------------------------------------------
    # Cash generation
    # --------------------------------------------------

    free_cash_flow = financial_data.get("free_cash_flow")
    operating_cash_flow = financial_data.get("operating_cash_flow")

    if free_cash_flow is not None and operating_cash_flow is not None:

        if free_cash_flow > 0 and operating_cash_flow > 0:
            analysis["cash_generation"] = "Strong"
        elif operating_cash_flow > 0:
            analysis["cash_generation"] = "Positive"
        else:
            analysis["cash_generation"] = "Weak"
            analysis["risk_flags"].append("Weak operating cash flow")

    return analysis