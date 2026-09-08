import yfinance as yf


def get_stock_summary(ticker: str) -> dict:
    """
    Retrieve key financial information for a company.
    """

    ticker = ticker.upper().strip()

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        # Company
        "company_name": info.get("longName"),
        "ticker": ticker,
        "sector": info.get("sector"),
        "industry": info.get("industry"),

        # Market
        "current_price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),

        # Profitability
        "revenue": info.get("totalRevenue"),
        "net_income": info.get("netIncomeToCommon"),
        "profit_margin": info.get("profitMargins"),
        "operating_margin": info.get("operatingMargins"),
        "return_on_equity": info.get("returnOnEquity"),
        "return_on_assets": info.get("returnOnAssets"),

        # Growth
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),

        # Valuation
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "price_to_book": info.get("priceToBook"),

        # Leverage / liquidity
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
        "quick_ratio": info.get("quickRatio"),

        # Cash flow
        "free_cash_flow": info.get("freeCashflow"),
        "operating_cash_flow": info.get("operatingCashflow"),
    }