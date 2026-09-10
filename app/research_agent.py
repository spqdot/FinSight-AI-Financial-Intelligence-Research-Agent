from app.tools import get_stock_summary
from app.financial_analysis import analyze_financial_health
from app.historical_analysis import get_historical_financials
from app.risk_analysis import analyze_risk
from app.agents import analyze_company


def research_company(ticker: str) -> str:
    """
    Run the complete FinSight financial research pipeline
    for a single company.
    """

    ticker = ticker.upper().strip()

    # 1. Retrieve current financial data
    stock_data = get_stock_summary(ticker)

    # 2. Analyze financial health
    financial_health = analyze_financial_health(stock_data)

    # 3. Analyze historical financial performance
    historical_data = get_historical_financials(ticker)

    # 4. Analyze financial and market risk
    risk_data = analyze_risk(
        stock_data,
        historical_data
    )

    # 5. Generate AI-powered research report
    ai_report = analyze_company(
        stock_data,
        financial_health,
        historical_data,
        risk_data
    )

    return ai_report