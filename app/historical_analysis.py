import yfinance as yf
import pandas as pd


def get_historical_financials(ticker: str, years: int = 5):
    """
    Retrieve historical financial data and calculate
    key growth and performance metrics.
    """

    stock = yf.Ticker(ticker)

    # -----------------------------
    # Income statement
    # -----------------------------
    income_statement = stock.income_stmt

    if income_statement.empty:
        raise ValueError(f"No financial data found for {ticker}")

    # Keep the most recent years
    income_statement = income_statement.iloc[:, :years]

    # Revenue
    revenue = income_statement.loc["Total Revenue"]

    # Net income
    net_income = income_statement.loc["Net Income"]

    # -----------------------------
    # Calculate CAGR
    # -----------------------------
    def calculate_cagr(series):
        series = series.dropna()

        if len(series) < 2:
            return None

        beginning = float(series.iloc[-1])
        ending = float(series.iloc[0])
        periods = len(series) - 1

        if beginning <= 0 or ending <= 0:
            return None

        return (ending / beginning) ** (1 / periods) - 1

    revenue_cagr = calculate_cagr(revenue)
    earnings_cagr = calculate_cagr(net_income)

    # -----------------------------
    # Profit margin
    # -----------------------------
    profit_margin = net_income / revenue

    # -----------------------------
    # Stock price history
    # -----------------------------
    history = stock.history(period="5y")

    if history.empty:
        stock_return = None
        volatility = None
    else:
        start_price = float(history["Close"].iloc[0])
        end_price = float(history["Close"].iloc[-1])

        stock_return = (end_price / start_price) - 1

        daily_returns = history["Close"].pct_change().dropna()

        volatility = float(
            daily_returns.std() * (252 ** 0.5)
        )

    # -----------------------------
    # Format financial history
    # -----------------------------
    financial_history = []

    for date in revenue.index:
        financial_history.append(
            {
                "year": str(date.year),
                "revenue": float(revenue.loc[date]),
                "net_income": float(net_income.loc[date]),
                "profit_margin": round(
                    float(profit_margin.loc[date]), 4
                )
            }
        )

    return {
        "ticker": ticker.upper(),
        "years_analyzed": len(financial_history),
        "financial_history": financial_history,
        "revenue_cagr": (
            round(revenue_cagr, 4)
            if revenue_cagr is not None
            else None
        ),
        "net_income_cagr": (
            round(earnings_cagr, 4)
            if earnings_cagr is not None
            else None
        ),
        "stock_return_5y": (
            round(stock_return, 4)
            if stock_return is not None
            else None
        ),
        "annualized_volatility": (
            round(volatility, 4)
            if volatility is not None
            else None
        )
    }