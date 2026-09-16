import yfinance as yf
import pandas as pd
from datetime import date, timedelta


def get_historical_financials(
    ticker: str,
    years: int = 5,
    analysis_date: str | None = None,
):
    """
    Retrieve historical financial data and calculate
    key growth, stock performance, market return metrics,
    and historical stock prices.

    analysis_date:
        Optional date in YYYY-MM-DD format.
        If provided, market returns and price history are
        calculated relative to that date. Otherwise, today's
        latest available market date is used.
    """

    ticker = ticker.upper().strip()

    if not ticker:
        raise ValueError("Ticker symbol cannot be empty.")

    stock = yf.Ticker(ticker)

    # ---------------------------------------------------------
    # Determine analysis date
    # ---------------------------------------------------------

    if analysis_date:
        try:
            target_date = date.fromisoformat(analysis_date)
        except ValueError:
            raise ValueError(
                "analysis_date must use YYYY-MM-DD format."
            )
    else:
        target_date = date.today()

    if target_date > date.today():
        raise ValueError(
            "analysis_date cannot be in the future."
        )

    # ---------------------------------------------------------
    # Income statement
    # ---------------------------------------------------------

    income_statement = stock.income_stmt

    if income_statement.empty:
        raise ValueError(
            f"No financial data found for {ticker}"
        )

    income_statement = income_statement.iloc[:, :years]

    required_rows = ["Total Revenue", "Net Income"]

    for row in required_rows:
        if row not in income_statement.index:
            raise ValueError(
                f"{row} not available for {ticker}"
            )

    revenue = income_statement.loc["Total Revenue"]
    net_income = income_statement.loc["Net Income"]

    # ---------------------------------------------------------
    # CAGR
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Profit margin
    # ---------------------------------------------------------

    profit_margin = net_income / revenue

    financial_history = []

    for current_date in revenue.index:

        if current_date in net_income.index:

            financial_history.append(
                {
                    "year": str(current_date.year),
                    "revenue": float(
                        revenue.loc[current_date]
                    ),
                    "net_income": float(
                        net_income.loc[current_date]
                    ),
                    "profit_margin": round(
                        float(
                            profit_margin.loc[current_date]
                        ),
                        4,
                    ),
                }
            )

    # ---------------------------------------------------------
    # Historical stock price
    #
    # Yahoo Finance `end` is exclusive, so request one
    # additional day.
    # ---------------------------------------------------------

    history_start = target_date.replace(
        year=target_date.year - years
    )

    history_end = target_date + timedelta(days=1)

    history = stock.history(
        start=history_start,
        end=history_end,
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(
            f"No stock price history found for {ticker} "
            f"around {target_date.isoformat()}"
        )

    # Remove timezone from index if present
    price_history = history.copy()

    if price_history.index.tz is not None:
        price_history.index = (
            price_history.index.tz_localize(None)
        )

    # Keep only prices up to selected analysis date
    price_history = price_history[
        price_history.index.date <= target_date
    ]

    if price_history.empty:
        raise ValueError(
            f"No trading data available for {ticker} "
            f"on or before {target_date.isoformat()}"
        )

    # ---------------------------------------------------------
    # Historical price series for frontend chart
    # ---------------------------------------------------------

    historical_prices = []

    for current_date, row in price_history.iterrows():

        close_price = row.get("Close")

        if pd.notna(close_price):

            historical_prices.append(
                {
                    "date": current_date.strftime(
                        "%Y-%m-%d"
                    ),
                    "close": round(
                        float(close_price),
                        2,
                    ),
                }
            )

    # ---------------------------------------------------------
    # Latest available trading-day price
    # ---------------------------------------------------------

    end_price = float(
        price_history["Close"].iloc[-1]
    )

    # ---------------------------------------------------------
    # Helper: return between two dates
    # ---------------------------------------------------------

    def calculate_period_return(start_date):

        period_data = price_history[
            price_history.index.date >= start_date
        ]

        if period_data.empty:
            return None

        start_price = float(
            period_data["Close"].iloc[0]
        )

        if start_price <= 0:
            return None

        return (end_price / start_price) - 1

    # ---------------------------------------------------------
    # Market return periods
    # ---------------------------------------------------------

    month_start = target_date.replace(day=1)

    year_start = target_date.replace(
        month=1,
        day=1,
    )

    three_month_start = (
        pd.Timestamp(target_date)
        - pd.DateOffset(months=3)
    ).date()

    six_month_start = (
        pd.Timestamp(target_date)
        - pd.DateOffset(months=6)
    ).date()

    one_year_start = (
        pd.Timestamp(target_date)
        - pd.DateOffset(years=1)
    ).date()

    three_year_start = (
        pd.Timestamp(target_date)
        - pd.DateOffset(years=3)
    ).date()

    five_year_start = (
        pd.Timestamp(target_date)
        - pd.DateOffset(years=5)
    ).date()

    market_returns = {
        "mtd_return": calculate_period_return(
            month_start
        ),
        "ytd_return": calculate_period_return(
            year_start
        ),
        "three_month_return": calculate_period_return(
            three_month_start
        ),
        "six_month_return": calculate_period_return(
            six_month_start
        ),
        "one_year_return": calculate_period_return(
            one_year_start
        ),
        "three_year_return": calculate_period_return(
            three_year_start
        ),
        "five_year_return": calculate_period_return(
            five_year_start
        ),
    }

    # ---------------------------------------------------------
    # Round market returns
    # ---------------------------------------------------------

    for key in market_returns:

        if market_returns[key] is not None:
            market_returns[key] = round(
                market_returns[key],
                4,
            )

    # ---------------------------------------------------------
    # 5-year stock return
    # ---------------------------------------------------------

    five_year_return = market_returns[
        "five_year_return"
    ]

    # ---------------------------------------------------------
    # Annualized volatility
    #
    # Calculated from available 5-year price history.
    # ---------------------------------------------------------

    daily_returns = (
        price_history["Close"]
        .pct_change()
        .dropna()
    )

    if len(daily_returns) > 1:

        volatility = float(
            daily_returns.std()
            * (252 ** 0.5)
        )

        volatility = round(
            volatility,
            4,
        )

    else:
        volatility = None

    # ---------------------------------------------------------
    # Return final result
    # ---------------------------------------------------------

    return {
        "ticker": ticker,
        "analysis_date": target_date.isoformat(),

        "years_analyzed": len(
            financial_history
        ),

        "financial_history": financial_history,

        # Historical daily prices for frontend charts
        "price_history": historical_prices,

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
            round(five_year_return, 4)
            if five_year_return is not None
            else None
        ),

        "annualized_volatility": volatility,

        "market_returns": market_returns,
    }