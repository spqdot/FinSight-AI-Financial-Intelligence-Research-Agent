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
def chat_with_finsight(
    question: str,
    stock_data: dict | None = None,
    financial_health: dict | None = None,
    historical_data: dict | None = None,
    risk_data: dict | None = None,
) -> str:
    """
    Generate an AI chatbot response using verified FinSight financial data.
    """

    llm = ChatOpenAI(
        api_key=OPENAI_API_KEY,
        model="gpt-4o-mini",
        temperature=0,
    )

    context = {
        "stock_data": stock_data or {},
        "financial_health": financial_health or {},
        "historical_data": historical_data or {},
        "risk_data": risk_data or {},
    }

    prompt = f"""
You are FinSight AI, a financial research assistant.

Answer the user's question clearly and concisely.

IMPORTANT RULES:

1. Use ONLY the verified financial data provided in the context.
2. Do not invent financial metrics, prices, earnings, growth rates,
   valuation ratios, or historical performance.
3. Clearly distinguish between factual financial data and interpretation.
4. Do not claim to know future stock prices.
5. Do not claim that there is one exact "right time" to buy a stock.
6. For questions about buying or selling shares, provide objective
   financial analysis and decision-support factors rather than a
   personalized buy/sell recommendation.
7. Explain factors investors could consider, such as:
   - valuation
   - earnings growth
   - profitability
   - financial health
   - historical performance
   - volatility
   - risk
   - potential downside
8. If the available data is insufficient to answer the question,
   explicitly say so.
9. Keep the answer understandable to a general user.
10. Never invent information outside the supplied context.

VERIFIED FINSIGHT DATA:

{json.dumps(context, indent=2, default=str)}

USER QUESTION:

{question}

Answer the user directly.

If the question is about buying or selling, structure the answer
around evidence and factors to consider rather than giving a direct
personalized investment instruction.
"""

    response = llm.invoke(prompt)

    return response.content