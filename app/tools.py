import yfinance as yf


def get_stock_summary(ticker: str) -> dict:
    """
    Retrieve key financial information for a company.
    """

    ticker = ticker.upper().strip()

    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    stock = yf.Ticker(ticker)

    try:
        info = stock.info
    except Exception as e:
        raise RuntimeError(
            f"Failed to retrieve Yahoo Finance data for {ticker}: {e}"
        ) from e

    if not info:
        raise RuntimeError(
            f"No financial information returned by Yahoo Finance for {ticker}."
        )

    # Detect the specific situation we're currently seeing on Render.
    if not any(
        info.get(field)
        for field in ["longName", "currentPrice", "marketCap", "totalRevenue"]
    ):
        available_keys = list(info.keys())

        raise RuntimeError(
            f"Yahoo Finance returned incomplete data for {ticker}. "
            f"Received {len(available_keys)} fields. "
            f"Available fields: {available_keys[:20]}"
        )

    # EPS
    trailing_eps = info.get("trailingEps")
    forward_eps = info.get("forwardEps")

    # Calculate EPS growth when both values are available.
    eps_growth = None

    if trailing_eps is not None and forward_eps is not None:
        if trailing_eps != 0:
            eps_growth = (forward_eps - trailing_eps) / abs(trailing_eps)

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

        # Earnings
        "trailing_eps": trailing_eps,
        "forward_eps": forward_eps,
        "eps_growth": eps_growth,

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