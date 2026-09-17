from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from app.tools import get_stock_summary
from app.financial_analysis import analyze_financial_health
from app.historical_analysis import get_historical_financials
from app.risk_analysis import analyze_risk
from app.agents import analyze_company, chat_with_finsight
from app.comparison import compare_companies
from app.comparison_agent import compare_companies_with_ai


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="FinSight AI",
    description=(
        "Financial Intelligence & Research Agent API "
        "for company analysis and comparative financial research."
    ),
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://fin-sight-ai-financial-intelligence.vercel.app",
        "https://fin-sight-ai-financial-intelligence-research-agent-7oora62l.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Request Models
# ============================================================

class ResearchRequest(BaseModel):
    ticker: str = Field(
        ...,
        min_length=1,
        description="Stock ticker symbol, e.g. MSFT"
    )

    analysis_date: Optional[str] = Field(
        default=None,
        description="Optional analysis date in YYYY-MM-DD format"
    )


class ComparisonRequest(BaseModel):
    tickers: List[str] = Field(
        ...,
        min_length=2,
        description="List of at least two stock ticker symbols",
        examples=[["MSFT", "AAPL", "TSLA"]],
    )

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User's financial research question",
    )
    ticker: Optional[str] = Field(
        default=None,
        description="Optional stock ticker to provide company context",
    )

# ============================================================
# Response Models
# ============================================================

class StockData(BaseModel):
    company_name: Optional[str] = None
    ticker: str
    sector: Optional[str] = None
    industry: Optional[str] = None

    current_price: Optional[float] = None
    market_cap: Optional[float] = None
    revenue: Optional[float] = None
    net_income: Optional[float] = None

    profit_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    return_on_equity: Optional[float] = None
    return_on_assets: Optional[float] = None

    # Earnings
    trailing_eps: Optional[float] = None
    forward_eps: Optional[float] = None
    eps_growth: Optional[float] = None

    # Growth
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None

    pe_ratio: Optional[float] = None
    forward_pe: Optional[float] = None
    price_to_book: Optional[float] = None

    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None

    free_cash_flow: Optional[float] = None
    operating_cash_flow: Optional[float] = None


class FinancialHealth(BaseModel):
    profitability: str
    growth: str
    capital_efficiency: str
    liquidity: str
    leverage: str
    valuation: str
    cash_generation: str
    risk_flags: List[str]


class MarketReturns(BaseModel):
    mtd_return: Optional[float] = None
    ytd_return: Optional[float] = Noneapp.add_middleware(
    three_month_return: Optional[float] = None
    six_month_return: Optional[float] = None
    one_year_return: Optional[float] = None
    three_year_return: Optional[float] = None
    five_year_return: Optional[float] = None


class HistoricalAnalysis(BaseModel):
    revenue_cagr: Optional[float] = None
    net_income_cagr: Optional[float] = None
    stock_return_5y: Optional[float] = None
    annualized_volatility: Optional[float] = None
    price_history: Optional[list[dict]] = None
    market_returns: Optional[MarketReturns] = None


class RiskAnalysis(BaseModel):
    risk_level: str
    risk_score: float
    risk_flags: List[str]


class ResearchResponse(BaseModel):
    ticker: str
    stock_data: StockData
    financial_health: FinancialHealth
    historical_analysis: HistoricalAnalysis
    risk_analysis: RiskAnalysis
    ai_report: str


class ComparisonCompany(BaseModel):
    ticker: str
    company_name: Optional[str] = None

    current_price: Optional[float] = None
    market_cap: Optional[float] = None

    profit_margin: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    return_on_equity: Optional[float] = None

    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    pe_ratio: Optional[float] = None

    free_cash_flow: Optional[float] = None

    revenue_cagr: Optional[float] = None
    net_income_cagr: Optional[float] = None
    stock_return_5y: Optional[float] = None
    volatility: Optional[float] = None

    financial_health: FinancialHealth
    risk: RiskAnalysis


class ComparisonData(BaseModel):
    companies: List[ComparisonCompany]


class ComparisonResponse(BaseModel):
    tickers: List[str]
    comparison: ComparisonData
    ai_report: str


# ============================================================
# Health Endpoints
# ============================================================

@app.get("/")
def root():
    return {
        "message": "FinSight AI API is running",
        "version": "1.0.0",
        "status": "healthy",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# Company Research Endpoint
# ============================================================

@app.post(
    "/research",
    response_model=ResearchResponse,
)
def research(request: ResearchRequest):

    ticker = request.ticker.upper().strip()

    if not ticker:
        raise HTTPException(
            status_code=400,
            detail="Ticker symbol cannot be empty.",
        )

    try:
        # 1. Retrieve financial data
        stock_data = get_stock_summary(ticker)

        # 2. Financial health analysis
        financial_health = analyze_financial_health(stock_data)

        # 3. Historical financial analysis
        historical_data = get_historical_financials(
            ticker,
            analysis_date=request.analysis_date,
        )

        # 4. Risk analysis
        risk_data = analyze_risk(
            stock_data,
            historical_data,
        )

        # 5. AI-powered research report
        ai_report = analyze_company(
            stock_data,
            financial_health,
            historical_data,
            risk_data,
        )

        return {
            "ticker": ticker,
            "stock_data": stock_data,
            "financial_health": financial_health,
            "historical_analysis": historical_data,
            "risk_analysis": risk_data,
            "ai_report": ai_report,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed for {ticker}: {str(e)}",
        )

# ============================================================
# Chat with FinSight AI Endpoint
# ============================================================
@app.post("/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty.",
        )

    ticker = request.ticker.strip().upper() if request.ticker else None

    stock_data = {}
    financial_health = {}
    historical_data = {}
    risk_data = {}

    if ticker:
        try:
            stock_data = get_stock_summary(ticker)

            financial_health = analyze_financial_health(
                stock_data
            )

            historical_data = get_historical_financials(
                ticker
            )

            risk_data = analyze_risk(
                stock_data,
                historical_data,
            )

        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to load data for {ticker}: {str(exc)}",
            )

    answer = chat_with_finsight(
        question=question,
        stock_data=stock_data,
        financial_health=financial_health,
        historical_data=historical_data,
        risk_data=risk_data,
    )

    return {
        "question": question,
        "ticker": ticker,
        "answer": answer,
    }
# ============================================================
# Company Comparison Endpoint
# ============================================================

@app.post(
    "/compare",
    response_model=ComparisonResponse,
)
def compare(request: ComparisonRequest):

    tickers = [
        ticker.upper().strip()
        for ticker in request.tickers
        if ticker.strip()
    ]

    if len(tickers) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two valid tickers are required.",
        )

    try:
        # 1. Deterministic comparison
        comparison_data = compare_companies(tickers)

        # 2. AI-powered comparison
        ai_report = compare_companies_with_ai(tickers)

        return {
            "tickers": tickers,
            "comparison": comparison_data,
            "ai_report": ai_report,
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comparison failed: {str(e)}",
        )