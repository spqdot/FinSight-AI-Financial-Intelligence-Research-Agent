# FinSight AI — Financial Intelligence & Research Agent

FinSight AI is an AI-powered financial research application that combines financial data analysis, historical performance analysis, valuation metrics, risk analysis, company comparison, and an LLM-powered financial research assistant in a single web application.

The project is designed to turn financial data into structured, understandable insights while keeping AI analysis grounded in verified data.

## Live Application

- Frontend: https://fin-sight-ai-financial-intelligence.vercel.app
- Backend API: https://finsight-ai-financial-intelligence.onrender.com
- API documentation: https://finsight-ai-financial-intelligence.onrender.com/docs

## Features

- **Company Financial Analysis**
  - Revenue and earnings
  - Profitability margins
  - ROE and ROA
  - Liquidity and leverage
  - Free cash flow and operating cash flow

- **Financial Health Analysis**
  - Profitability
  - Growth
  - Capital efficiency
  - Liquidity
  - Leverage
  - Valuation
  - Cash generation
  - Risk flags

- **Historical Performance**
  - Historical stock-price chart
  - 5-year stock return
  - Annualized volatility
  - Revenue CAGR
  - Net income CAGR
  - Market performance comparison

- **Valuation Analysis**
  - P/E ratio
  - Forward P/E
  - Price-to-book ratio
  - Other available financial indicators

- **Risk Analysis**
  - Risk score
  - Risk level
  - Market volatility indicators
  - Financial risk flags

- **Company Comparison**
  - Compare multiple companies using financial and risk metrics
  - Deterministic financial comparison
  - AI-generated comparison insights

- **FinSight AI Chatbot**
  - Ask natural-language questions about a company
  - Uses verified financial context from the application
  - Provides objective financial analysis and decision-support factors
  - Avoids unsupported financial claims and future price predictions

- **Interactive Web Interface**
  - Next.js frontend
  - Interactive charts with Recharts
  - Company and date selection
  - Financial metric cards and health indicators

## Architecture

```text
                         ┌─────────────────────────┐
                         │       Next.js UI        │
                         │      React + Recharts   │
                         └────────────┬────────────┘
                                      │
                                      │ REST API
                                      ▼
                         ┌─────────────────────────┐
                         │      FastAPI Backend    │
                         │                         │
                         │  /research              │
                         │  /compare               │
                         │  /chat                  │
                         └────────────┬────────────┘
                                      │
                 ┌────────────────────┼────────────────────┐
                 │                    │                    │
                 ▼                    ▼                    ▼
          Financial Data       Analysis Modules       OpenAI LLM
          & Market Data        Health / Risk /        AI Research
                               Historical Analysis    Assistant
                 │                    │                    │
                 └────────────────────┼────────────────────┘
                                      ▼
                              Structured Insights
```

## Tech Stack

### Backend

- Python
- FastAPI
- Pydantic
- Uvicorn
- Pandas
- NumPy
- yfinance
- LangChain
- LangGraph
- OpenAI API

### Frontend

- Next.js
- React
- TypeScript
- Recharts
- Tailwind CSS

### Deployment

- Render — FastAPI backend
- Vercel — Next.js frontend

## Project Structure

```text
FinSight-AI-Financial-Intelligence-Research-Agent/
│
├── app/
│   ├── agents.py
│   ├── comparison.py
│   ├── comparison_agent.py
│   ├── config.py
│   ├── financial_analysis.py
│   ├── historical_analysis.py
│   ├── main.py
│   ├── report_generator.py
│   ├── research_agent.py
│   ├── risk_analysis.py
│   └── tools.py
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── components/
│   ├── lib/
│   │   └── api.ts
│   ├── package.json
│   └── package-lock.json
│
├── .env
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/spqdot/FinSight-AI-Financial-Intelligence-Research-Agent.git
cd FinSight-AI-Financial-Intelligence-Research-Agent
```

### 2. Create a Python virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key
```

**Do not commit your `.env` file or expose your API key.**

### 5. Start the FastAPI backend

From the project root:

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

### 6. Install frontend dependencies

Open another terminal:

```bash
cd frontend
npm install
```

For local development, create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 7. Start the frontend

```bash
npm run dev
```

Open:

```text
http://localhost:3000
```

## API Endpoints

### Research a company

```text
POST /research
```

Example request:

```json
{
  "ticker": "MSFT"
}
```

The research endpoint combines financial metrics, financial health, historical analysis, risk analysis, and AI-generated research insights.

### Compare companies

```text
POST /compare
```

Example request:

```json
{
  "tickers": ["MSFT", "AAPL", "TSLA"]
}
```

### Ask FinSight AI

```text
POST /chat
```

Example request:

```json
{
  "question": "What are the main strengths and risks?",
  "ticker": "MSFT"
}
```

The chatbot receives the company's verified financial context and generates a natural-language response.

## Example Questions

Users can ask questions such as:

- What are the main strengths and risks?
- How is the company valued?
- How has the stock performed historically?
- What should I consider before buying?
- What is driving the company's earnings growth?
- How profitable is the company?
- How do trailing and forward EPS compare?
- Is the company's financial health strong?
- How much debt does the company have?
- How volatile has the stock been?
- What are the key valuation metrics?
- What factors could affect future performance?

## AI Safety & Data-Grounded Analysis

FinSight AI is designed as a **financial research and decision-support tool**, not as a personalized investment advisor.

The AI assistant is instructed to:

- Use only the financial data supplied by FinSight.
- Avoid inventing metrics or financial facts.
- Distinguish factual data from interpretation.
- Avoid predicting future stock prices.
- Avoid presenting a single exact time as the "right" time to buy a stock.
- Provide factors and evidence that users can consider when evaluating an investment decision.

## Deployment

The application is structured as two deployable services:

```text
Frontend → Vercel
Backend  → Render
```

The frontend uses the `NEXT_PUBLIC_API_URL` environment variable to connect to the FastAPI backend.

For production, configure the backend URL in the frontend deployment environment rather than committing environment-specific secrets to the repository.

## Future Improvements

Planned improvements include:

- Expanded company comparison interface
- Transparent FinSight scoring and explainability
- LangGraph-based agent workflows and tool calling
- SEC filings and annual-report retrieval
- RAG over financial documents and earnings-call transcripts
- Source citations in AI-generated answers
- Automated testing and improved error handling
- Caching and performance optimization
- Docker-based deployment

## Disclaimer

FinSight AI is an educational and research-oriented software project. The information and analysis produced by the application are not financial advice, investment recommendations, or guarantees of future performance. Users should independently evaluate financial information and consult a qualified financial professional when appropriate.

## Author

**Shrabani Panigrahi**

AI Engineering & Data Science | Python | Machine Learning | Generative AI | RAG

GitHub: https://github.com/spqdot
