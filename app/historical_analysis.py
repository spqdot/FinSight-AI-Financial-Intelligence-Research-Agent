import yfinance as yf
import pandas as pd


def get_historical_financials(ticker: str, years: int = 5):
    """
    Retrieve historical financial data and calculate
    key growth and market performance metrics.
    """

    ticker = ticker.upper().strip()
    stock = yf.Ticker(ticker)

    # -----------------------------
    # Income statement
    # -----------------------------
    income_statement = stock.income_stmt

    if income_statement.empty:
        raise ValueError(f"No financial data found for {ticker}")

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
        stock_return_5y = None
        annualized_volatility = None
        market_returns = {}
    else:

        # Make dates timezone-naive for easier comparison
        history.index = history.index.tz_localize(None)

        close_prices = history["Close"].dropna()

        latest_price = float(close_prices.iloc[-1])
        latest_date = close_prices.index[-1]

        # -----------------------------
        # Period return helper
        # -----------------------------
        def calculate_period_return(start_date):
            prices = close_prices[close_prices.index >= start_date]

            if prices.empty:
                return None

            start_price = float(prices.iloc[0])

            return (latest_price / start_price) - 1

        # -----------------------------
        # Current dates
        # -----------------------------
        latest_day = latest_date.date()

        month_start = pd.Timestamp(
            year=latest_date.year,
            month=latest_date.month,
            day=1
        )

        year_start = pd.Timestamp(
            year=latest_date.year,
            month=1,
            day=1
        )

        # -----------------------------
        # Market performance
        # -----------------------------
        mtd_return = calculate_period_return(month_start)
        ytd_return = calculate_period_return(year_start)

        three_month_return = calculate_period_return(
            latest_date - pd.DateOffset(months=3)
        )

        six_month_return = calculate_period_return(
            latest_date - pd.DateOffset(months=6)
        )

        one_year_return = calculate_period_return(
            latest_date - pd.DateOffset(years=1)
        )

        three_year_return = calculate_period_return(
            latest_date - pd.DateOffset(years=3)
        )

        five_year_return = calculate_period_return(
            latest_date - pd.DateOffset(years=5)
        )

        market_returns = {
            "mtd_return": mtd_return,
            "ytd_return": ytd_return,
            "three_month_return": three_month_return,
            "six_month_return": six_month_return,
            "one_year_return": one_year_return,
            "three_year_return": three_year_return,
            "five_year_return": five_year_return,
        }

        # -----------------------------
        # Annualized volatility
        # -----------------------------
        daily_returns = close_prices.pct_change().dropna()

        annualized_volatility = float(
            daily_returns.std() * (252 ** 0.5)
        )

        # Keep 5Y return consistent with existing API
        stock_return_5y = five_year_return

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
                    float(profit_margin.loc[date]),
                    4
                )
            }
        )

    # -----------------------------
    # Return result
    # -----------------------------
    return {
        "ticker": ticker,
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
            round(stock_return_5y, 4)
            if stock_return_5y is not None
            else None
        ),

        "annualized_volatility": (
            round(annualized_volatility, 4)
            if annualized_volatility is not None
            else None
        ),

        "market_returns": {
            key: (
                round(value, 4)
                if value is not None
                else None
            )
            for key, value in market_returns.items()
        }
    }