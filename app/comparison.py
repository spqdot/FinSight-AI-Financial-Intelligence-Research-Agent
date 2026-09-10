from app.tools import get_stock_summary
from app.financial_analysis import analyze_financial_health
from app.historical_analysis import get_historical_financials
from app.risk_analysis import analyze_risk


def compare_companies(tickers: list[str]) -> dict:
    """
    Retrieve and compare financial metrics
    for multiple companies.
    """

    if len(tickers) < 2:
        raise ValueError("At least two companies are required.")

    companies = []

    for ticker in tickers:

        ticker = ticker.upper().strip()

        # 1. Current financial data
        stock_data = get_stock_summary(ticker)

        # 2. Financial health
        financial_health = analyze_financial_health(
            stock_data
        )

        # 3. Historical performance
        historical_data = get_historical_financials(
            ticker
        )

        # 4. Risk analysis
        risk_data = analyze_risk(
            stock_data,
            historical_data
        )

        companies.append({
            "ticker": ticker,
            "company_name": stock_data.get("company_name"),

            "current_price": stock_data.get("current_price"),
            "market_cap": stock_data.get("market_cap"),

            "profit_margin": stock_data.get("profit_margin"),
            "revenue_growth": stock_data.get("revenue_growth"),
            "earnings_growth": stock_data.get("earnings_growth"),

            "return_on_equity": stock_data.get(
                "return_on_equity"
            ),

            "debt_to_equity": stock_data.get(
                "debt_to_equity"
            ),

            "current_ratio": stock_data.get(
                "current_ratio"
            ),

            "pe_ratio": stock_data.get(
                "pe_ratio"
            ),

            "free_cash_flow": stock_data.get(
                "free_cash_flow"
            ),

            "revenue_cagr": historical_data.get(
                "revenue_cagr"
            ),

            "net_income_cagr": historical_data.get(
                "net_income_cagr"
            ),

            "stock_return_5y": historical_data.get(
                "5y_stock_return"
            ),

            "volatility": historical_data.get(
                "annualized_volatility"
            ),

            "financial_health": financial_health,

            "risk": risk_data
        })

    return {
        "companies": companies
    }