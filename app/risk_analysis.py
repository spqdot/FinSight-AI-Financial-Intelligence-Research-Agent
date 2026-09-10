def analyze_risk(stock_data: dict, historical_data: dict) -> dict:
    """
    Analyze financial and market risks using deterministic rules.
    """

    risk_flags = []
    risk_score = 0

    # --------------------------------------------------
    # Profitability risk
    # --------------------------------------------------

    profit_margin = stock_data.get("profit_margin")

    if profit_margin is not None:
        if profit_margin < 0:
            risk_flags.append("Negative profit margin")
            risk_score += 3
        elif profit_margin < 0.05:
            risk_flags.append("Low profit margin")
            risk_score += 2

    # --------------------------------------------------
    # Revenue growth risk
    # --------------------------------------------------

    revenue_growth = stock_data.get("revenue_growth")

    if revenue_growth is not None:
        if revenue_growth < 0:
            risk_flags.append("Declining revenue")
            risk_score += 3
        elif revenue_growth < 0.05:
            risk_flags.append("Weak revenue growth")
            risk_score += 1

    # --------------------------------------------------
    # Earnings growth risk
    # --------------------------------------------------

    earnings_growth = stock_data.get("earnings_growth")

    if earnings_growth is not None:
        if earnings_growth < 0:
            risk_flags.append("Declining earnings")
            risk_score += 3

    # --------------------------------------------------
    # Leverage risk
    # --------------------------------------------------

    debt_to_equity = stock_data.get("debt_to_equity")

    if debt_to_equity is not None:
        if debt_to_equity >= 150:
            risk_flags.append("Very high debt-to-equity")
            risk_score += 3
        elif debt_to_equity >= 100:
            risk_flags.append("High debt-to-equity")
            risk_score += 2
        elif debt_to_equity >= 50:
            risk_flags.append("Moderate leverage")
            risk_score += 1

    # --------------------------------------------------
    # Liquidity risk
    # --------------------------------------------------

    current_ratio = stock_data.get("current_ratio")

    if current_ratio is not None:
        if current_ratio < 1:
            risk_flags.append("Weak current ratio")
            risk_score += 3
        elif current_ratio < 1.2:
            risk_flags.append("Tight liquidity")
            risk_score += 1

    # --------------------------------------------------
    # Valuation risk
    # --------------------------------------------------

    pe_ratio = stock_data.get("pe_ratio")

    if pe_ratio is not None:
        if pe_ratio >= 50:
            risk_flags.append("Very high P/E valuation")
            risk_score += 3
        elif pe_ratio >= 35:
            risk_flags.append("High P/E valuation")
            risk_score += 2

    # --------------------------------------------------
    # Market volatility risk
    # --------------------------------------------------

    volatility = historical_data.get("annualized_volatility")

    if volatility is not None:
        if volatility >= 0.40:
            risk_flags.append("Very high market volatility")
            risk_score += 3
        elif volatility >= 0.30:
            risk_flags.append("High market volatility")
            risk_score += 2
        elif volatility >= 0.20:
            risk_flags.append("Moderate market volatility")
            risk_score += 1

    # --------------------------------------------------
    # Historical stock performance
    # --------------------------------------------------

    stock_return = historical_data.get("5y_stock_return")

    if stock_return is not None and stock_return < 0:
        risk_flags.append("Negative five-year stock return")
        risk_score += 2

    # --------------------------------------------------
    # Overall risk classification
    # --------------------------------------------------

    if risk_score <= 2:
        risk_level = "Low"
    elif risk_score <= 5:
        risk_level = "Moderate"
    elif risk_score <= 8:
        risk_level = "High"
    else:
        risk_level = "Very High"

    return {
        "risk_level": risk_level,
        "risk_score": risk_score,
        "risk_flags": risk_flags
    }