import os
import json

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def analyze_company(
    stock_data: dict,
    financial_health: dict,
    historical_data: dict,
    risk_data: dict
) -> str:
    """
    Generate an AI-powered financial research report
    using verified structured financial analysis.
    """

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
You are a professional financial research analyst.

Analyze the company using ONLY the verified structured data
provided below.

Do not invent financial metrics.
Do not make unsupported claims.
Do not provide buy, sell, or investment recommendations.

Clearly distinguish between:
- financial metrics
- analytical interpretation
- risk observations

COMPANY FINANCIAL DATA:
{json.dumps(stock_data, indent=2, default=str)}

FINANCIAL HEALTH ANALYSIS:
{json.dumps(financial_health, indent=2, default=str)}

HISTORICAL ANALYSIS:
{json.dumps(historical_data, indent=2, default=str)}

RISK ANALYSIS:
{json.dumps(risk_data, indent=2, default=str)}

Create a concise professional research report with these sections:

1. Executive Summary
2. Profitability
3. Growth
4. Capital Efficiency
5. Liquidity and Leverage
6. Valuation
7. Historical Performance
8. Risk Assessment
9. Key Strengths
10. Key Risk Considerations
11. Overall Assessment

Use the actual numerical values provided.
Avoid exaggerating what the metrics imply.
Do not introduce information that is not present in the supplied data.
"""

    response = llm.invoke(prompt)

    return response.content