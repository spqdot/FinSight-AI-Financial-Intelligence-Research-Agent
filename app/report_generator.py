def generate_financial_report(
    stock_data: dict,
    financial_health: dict,
    historical_data: dict,
    risk_analysis: dict
) -> str:
    """
    Generate a structured financial research report
    from deterministic financial analysis results.
    """

    ticker = stock_data.get("ticker", "N/A")
    company = stock_data.get("company_name", "Unknown Company")

    revenue_cagr = historical_data.get("revenue_cagr")
    earnings_cagr = historical_data.get("net_income_cagr")
    stock_return = historical_data.get("5y_stock_return")
    volatility = historical_data.get("annualized_volatility")

    risk_level = risk_analysis.get("risk_level", "N/A")
    risk_score = risk_analysis.get("risk_score", "N/A")
    risk_flags = risk_analysis.get("risk_flags", [])

    report = f"""
FINANCIAL RESEARCH REPORT
=========================

Company: {company}
Ticker: {ticker}

1. COMPANY OVERVIEW
------------------
Sector: {stock_data.get("sector", "N/A")}
Industry: {stock_data.get("industry", "N/A")}
Current Price: {stock_data.get("current_price", "N/A")}
Market Capitalization: {stock_data.get("market_cap", "N/A")}

2. FINANCIAL HEALTH
-------------------
Profitability: {financial_health.get("profitability", "N/A")}
Growth: {financial_health.get("growth", "N/A")}
Capital Efficiency: {financial_health.get("capital_efficiency", "N/A")}
Liquidity: {financial_health.get("liquidity", "N/A")}
Leverage: {financial_health.get("leverage", "N/A")}
Valuation: {financial_health.get("valuation", "N/A")}
Cash Generation: {financial_health.get("cash_generation", "N/A")}

Risk Flags:
{", ".join(financial_health.get("risk_flags", []))
 if financial_health.get("risk_flags")
 else "None"}

3. RISK ASSESSMENT
------------------
Risk Level: {risk_level}
Risk Score: {risk_score}

Risk Flags:
{chr(10).join(f"- {flag}" for flag in risk_flags)
 if risk_flags
 else "- None identified"}

4. HISTORICAL PERFORMANCE
-------------------------
Revenue CAGR: {format_percentage(revenue_cagr)}
Net Income CAGR: {format_percentage(earnings_cagr)}
5-Year Stock Return: {format_percentage(stock_return)}
Annualized Volatility: {format_percentage(volatility)}

5. KEY OBSERVATIONS
-------------------
"""

    observations = []

    if revenue_cagr is not None and revenue_cagr > 0.10:
        observations.append(
            "Revenue has demonstrated strong historical growth."
        )

    if earnings_cagr is not None and earnings_cagr > 0.10:
        observations.append(
            "Net income has grown strongly over the analyzed period."
        )

    if stock_return is not None and stock_return > 0:
        observations.append(
            "The stock generated a positive return over the five-year period."
        )

    if volatility is not None and volatility > 0.30:
        observations.append(
            "Historical price volatility indicates elevated market risk."
        )
    elif volatility is not None:
        observations.append(
            "Historical price volatility remains below the elevated-risk threshold."
        )

    if risk_flags:
        for flag in risk_flags:
            observations.append(
                f"Risk consideration identified: {flag}."
            )

    if not observations:
        observations.append(
            "Insufficient data to generate detailed observations."
        )

    for i, observation in enumerate(observations, 1):
        report += f"{i}. {observation}\n"

    return report


def format_percentage(value):
    """Convert decimal values to percentage strings."""

    if value is None:
        return "N/A"

    return f"{value * 100:.2f}%"