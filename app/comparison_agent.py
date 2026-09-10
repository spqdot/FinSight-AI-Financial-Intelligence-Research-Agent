from langchain_openai import ChatOpenAI

from app.config import OPENAI_API_KEY
from app.comparison import compare_companies


llm = ChatOpenAI(
    api_key=OPENAI_API_KEY,
    model="gpt-4o-mini",
    temperature=0
)


def compare_companies_with_ai(tickers: list[str]) -> str:
    """
    Generate an AI-powered comparison of multiple companies.

    Financial metrics and risk assessments are calculated
    deterministically before being passed to the LLM.
    """

    # Get structured financial comparison data
    comparison_data = compare_companies(tickers)

    companies = comparison_data["companies"]

    # Build a concise dataset for the LLM
    company_sections = []

    for company in companies:

        health = company["financial_health"]
        risk = company["risk"]

        section = f"""
Company: {company["company_name"]}
Ticker: {company["ticker"]}

Current Price: {company["current_price"]}
Market Capitalization: {company["market_cap"]}

Profit Margin: {company["profit_margin"]}
Revenue Growth: {company["revenue_growth"]}
Earnings Growth: {company["earnings_growth"]}

Return on Equity: {company["return_on_equity"]}
Debt to Equity: {company["debt_to_equity"]}
Current Ratio: {company["current_ratio"]}
P/E Ratio: {company["pe_ratio"]}
Free Cash Flow: {company["free_cash_flow"]}

Revenue CAGR: {company["revenue_cagr"]}
Net Income CAGR: {company["net_income_cagr"]}
5-Year Stock Return: {company["stock_return_5y"]}
Annualized Volatility: {company["volatility"]}

Financial Health:
- Profitability: {health["profitability"]}
- Growth: {health["growth"]}
- Capital Efficiency: {health["capital_efficiency"]}
- Liquidity: {health["liquidity"]}
- Leverage: {health["leverage"]}
- Valuation: {health["valuation"]}
- Cash Generation: {health["cash_generation"]}

Risk:
- Risk Level: {risk["risk_level"]}
- Risk Score: {risk["risk_score"]}
- Risk Flags: {", ".join(risk["risk_flags"]) if risk["risk_flags"] else "None"}
"""

        company_sections.append(section)

    financial_information = "\n".join(company_sections)

    prompt = f"""
You are FinSight AI, a financial research assistant.

Compare the following companies using ONLY the financial
information and deterministic analysis provided below.

{financial_information}

Produce a structured research comparison with exactly
these sections:

1. Executive Summary
2. Profitability Comparison
3. Growth Comparison
4. Capital Efficiency Comparison
5. Liquidity and Leverage Comparison
6. Valuation Comparison
7. Historical Performance Comparison
8. Risk Comparison
9. Key Strengths by Company
10. Key Risk Considerations
11. Overall Comparative Assessment

Requirements:

- Use only the provided information.
- Do not invent financial metrics.
- Do not introduce external financial information.
- Do not provide personalized investment advice.
- Do not tell the user which stock they should buy.
- Explain differences using the supplied metrics.
- Distinguish clearly between financial strength and stock-market performance.
- Treat the deterministic risk score and risk level as authoritative.
- If a metric is unavailable, explicitly state that it is unavailable.
- Use precise financial terminology.
- Keep the analysis concise but substantive.
"""

    response = llm.invoke(prompt)

    return response.content