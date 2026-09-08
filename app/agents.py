from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY
from app.tools import get_stock_summary


llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0
)


def analyze_company(ticker: str) -> str:
    """
    Retrieve financial information and generate
    a concise financial analysis.
    """

    financial_data = get_stock_summary(ticker)

    prompt = f"""
You are FinSight AI, a financial research assistant.

Analyze the following company information.

Company:
{financial_data["company_name"]}

Ticker:
{financial_data["ticker"]}

Sector:
{financial_data["sector"]}

Industry:
{financial_data["industry"]}

Current Price:
{financial_data["current_price"]}

Market Capitalization:
{financial_data["market_cap"]}

Revenue:
{financial_data["revenue"]}

Net Income:
{financial_data["net_income"]}

Profit Margin:
{financial_data["profit_margin"]}

Return on Equity:
{financial_data["return_on_equity"]}

Debt to Equity:
{financial_data["debt_to_equity"]}

Provide:

1. Company overview
2. Revenue and profitability assessment
3. Capital efficiency assessment
4. Leverage assessment
5. Key financial observations

Do not invent financial information.
Only use the data provided above.
Clearly state when information is unavailable.
"""

    response = llm.invoke(prompt)

    return response.content