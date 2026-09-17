"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import MetricCard from "@/components/MetricCard";
import HealthBadge from "@/components/HealthBadge";
import {
  researchCompany,
  compareCompanies,
  chatCompany,
} from "@/lib/api";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell,
} from "recharts";

interface ResearchData {
  ticker: string;

  stock_data: {
    company_name: string | null;
    ticker: string;
    sector: string | null;
    industry: string | null;

    current_price: number | null;
    market_cap: number | null;
    revenue: number | null;
    net_income: number | null;

    profit_margin: number | null;
    operating_margin: number | null;
    return_on_equity: number | null;
    return_on_assets: number | null;

    // Earnings
    trailing_eps: number | null;
    forward_eps: number | null;
    eps_growth: number | null;

    // Growth
    revenue_growth: number | null;
    earnings_growth: number | null;

    pe_ratio: number | null;
    forward_pe: number | null;
    price_to_book: number | null;

    debt_to_equity: number | null;
    current_ratio: number | null;
    quick_ratio: number | null;

    free_cash_flow: number | null;
    operating_cash_flow: number | null;
  };

  financial_health: {
    profitability: string;
    growth: string;
    capital_efficiency: string;
    liquidity: string;
    leverage: string;
    valuation: string;
    cash_generation: string;
    risk_flags: string[];
  };

    historical_analysis: {
      analysis_date?: string | null;

      revenue_cagr: number | null;
      net_income_cagr: number | null;
      stock_return_5y: number | null;
      annualized_volatility: number | null;

      price_history?: {
        date: string;
        close: number;
      }[];

    market_returns?: {
      mtd_return: number | null;
      ytd_return: number | null;
      three_month_return: number | null;
      six_month_return: number | null;
      one_year_return: number | null;
      three_year_return: number | null;
      five_year_return: number | null;
    } | null;
  };

  risk_analysis: {
    risk_level: string;
    risk_score: number;
    risk_flags: string[];
  };

  ai_report: string;
}

/* -------------------------------------------------
   Formatting helpers
------------------------------------------------- */

function formatCurrency(value: number | null) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(value);
}

function formatLargeNumber(value: number | null) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  if (Math.abs(value) >= 1_000_000_000_000) {
    return `$${(value / 1_000_000_000_000).toFixed(2)}T`;
  }

  if (Math.abs(value) >= 1_000_000_000) {
    return `$${(value / 1_000_000_000).toFixed(2)}B`;
  }

  if (Math.abs(value) >= 1_000_000) {
    return `$${(value / 1_000_000).toFixed(2)}M`;
  }

  return `$${value.toLocaleString()}`;
}

function formatPercent(value: number | null) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  return `${(value * 100).toFixed(1)}%`;
}

function formatChartPercent(value: number | null) {
  if (value === null || value === undefined) {
    return 0;
  }

  return Number((value * 100).toFixed(2));
}

/* -------------------------------------------------
   Main page
------------------------------------------------- */

export default function Home() {
  const [ticker, setTicker] = useState("MSFT");

  const [research, setResearch] = useState<ResearchData | null>(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const [analysisDate, setAnalysisDate] = useState(
    new Date().toISOString().split("T")[0]
  );
  const [showAllCompanies, setShowAllCompanies] = useState(false);

  const [chatQuestion, setChatQuestion] = useState("");
  const [chatMessages, setChatMessages] = useState<
    {
      role: "user" | "assistant";
      content: string;
    }[]
  >([]);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [chatMessages]);
  const [chatLoading, setChatLoading] = useState(false);
  const [chatError, setChatError] = useState("");

  const [showResearchReport, setShowResearchReport] = useState(false);
  const popularCompanies = [
  { ticker: "MSFT", name: "Microsoft" },
  { ticker: "AAPL", name: "Apple" },
  { ticker: "NVDA", name: "NVIDIA" },
  { ticker: "GOOGL", name: "Alphabet" },
  { ticker: "AMZN", name: "Amazon" },
  { ticker: "META", name: "Meta" },
];

    const additionalCompanies = [
      // Technology
      { ticker: "ORCL", name: "Oracle" },
      { ticker: "CRM", name: "Salesforce" },
      { ticker: "ADBE", name: "Adobe" },

      // Semiconductors
      { ticker: "AMD", name: "AMD" },
      { ticker: "INTC", name: "Intel" },
      { ticker: "QCOM", name: "Qualcomm" },
      { ticker: "AVGO", name: "Broadcom" },
      { ticker: "TSM", name: "TSMC" },
      { ticker: "ASML", name: "ASML" },

      // Consumer
      { ticker: "TSLA", name: "Tesla" },
      { ticker: "WMT", name: "Walmart" },
      { ticker: "COST", name: "Costco" },
      { ticker: "MCD", name: "McDonald's" },
      { ticker: "KO", name: "Coca-Cola" },
      { ticker: "PEP", name: "PepsiCo" },

      // Financial
      { ticker: "JPM", name: "JPMorgan" },
      { ticker: "V", name: "Visa" },
      { ticker: "MA", name: "Mastercard" },
      { ticker: "BAC", name: "Bank of America" },
      { ticker: "GS", name: "Goldman Sachs" },

      // Healthcare
      { ticker: "LLY", name: "Eli Lilly" },
      { ticker: "JNJ", name: "Johnson & Johnson" },
      { ticker: "UNH", name: "UnitedHealth" },
      { ticker: "ABBV", name: "AbbVie" },
    ];
  async function handleResearch(event: FormEvent) {
    event.preventDefault();

    if (!ticker.trim()) {
      setError("Please enter a company ticker.");
      return;
    }

    setLoading(true);
    setError("");
    setResearch(null);

    try {
      const data = await researchCompany(
        ticker.trim().toUpperCase(),
        analysisDate
      );

      setResearch(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to retrieve company research."
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleChat(event: FormEvent) {
    event.preventDefault();

    if (!chatQuestion.trim()) {
      return;
    }

    setChatLoading(true);
    setChatError("");


    try {
     const question = chatQuestion.trim();

      const result = await chatCompany(
        question,
        ticker.trim().toUpperCase()
      );

      setChatMessages((previous) => [
        ...previous,
        {
          role: "user",
          content: question,
        },
        {
          role: "assistant",
          content: result.answer,
        },
      ]);

      setChatQuestion("");
    } catch (err) {
      setChatError(
        err instanceof Error
          ? err.message
          : "Unable to get an answer from FinSight AI."
      );
    } finally {
      setChatLoading(false);
    }
  }

  /* -------------------------------------------------
     Chart data
  ------------------------------------------------- */

  const marketReturns =
    research?.historical_analysis?.market_returns ?? {
      mtd_return: null,
      ytd_return: null,
      three_month_return: null,
      six_month_return: null,
      one_year_return: null,
      three_year_return: null,
      five_year_return: null,
    };

  const marketReturnData = [
    {
      period: "MTD",
      return: formatChartPercent(marketReturns.mtd_return),
    },
    {
      period: "YTD",
      return: formatChartPercent(marketReturns.ytd_return),
    },
    {
      period: "3M",
      return: formatChartPercent(marketReturns.three_month_return),
    },
    {
      period: "6M",
      return: formatChartPercent(marketReturns.six_month_return),
    },
    {
      period: "1Y",
      return: formatChartPercent(marketReturns.one_year_return),
    },
    {
      period: "3Y",
      return: formatChartPercent(marketReturns.three_year_return),
    },
    {
      period: "5Y",
      return: formatChartPercent(marketReturns.five_year_return),
    },
  ];

  return (
    <main className="min-h-screen bg-black text-white">

      {/* -------------------------------------------------
          Main container
      ------------------------------------------------- */}

      <div className="mx-auto max-w-7xl px-6 py-12">

        {/* -------------------------------------------------
            Hero
        ------------------------------------------------- */}

        <section className="mx-auto max-w-4xl text-center">

          

          <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
              FinSight AI
            </h2>

            <p className="mx-auto mt-4 max-w-3xl text-xl font-medium text-zinc-300">
              Financial Intelligence & Research Agent
            </p>

          <p className="mx-auto mt-5 max-w-3xl text-lg leading-8 text-zinc-400">
            Analyze company fundamentals, valuation, historical performance, risk,
            and financial health with AI-powered research.
          </p>

          {/* -------------------------------------------------
              Search
          ------------------------------------------------- */}

          <form
            onSubmit={handleResearch}
            className="mx-auto mt-8 max-w-4xl"
          >
            <div className="flex flex-col gap-3 lg:flex-row">

              <input
                type="text"
                value={ticker}
                onChange={(event) => setTicker(event.target.value)}
                placeholder="Enter ticker e.g. MSFT"
                className="min-w-0 flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-4 text-white outline-none transition focus:border-zinc-400"
              />

              <div className="flex items-center justify-between gap-3 rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-2 lg:min-w-[260px]">
                <label
                  htmlFor="analysis-date"
                  className="whitespace-nowrap text-xs text-zinc-500"
                >
                  Analysis Date
                </label>

                <input
                  id="analysis-date"
                  type="date"
                  value={analysisDate}
                  max={new Date().toISOString().split("T")[0]}
                  onChange={(event) =>
                    setAnalysisDate(event.target.value)
                  }
                  className="bg-transparent text-sm text-white outline-none"
                />
              </div>

              <button
                type="submit"
                disabled={loading}
                className="rounded-xl bg-white px-6 py-4 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {loading ? "Analyzing..." : "Analyze"}
              </button>

            </div>

            <p className="mt-2 text-left text-xs text-zinc-600">
              Historical returns are calculated using data available up to
              the selected date.
            </p>
          </form>

          {/* -------------------------------------------------
              Popular companies
          ------------------------------------------------- */}

       <div className="mx-auto mt-6 max-w-4xl">

          {/* Popular companies */}
          <div>
            <p className="mb-3 text-xs font-medium uppercase tracking-wider text-zinc-500">
              Popular Companies
            </p>

            <div className="flex flex-wrap justify-center gap-2">
              {popularCompanies.map((company) => (
                <button
                  key={company.ticker}
                  type="button"
                  onClick={() => {
                    setTicker(company.ticker);
                    setError("");
                  }}
                  className={`rounded-full border px-4 py-2 text-xs transition ${
                    ticker.toUpperCase() === company.ticker
                      ? "border-zinc-500 bg-zinc-800 text-white"
                      : "border-zinc-800 bg-zinc-950 text-zinc-400 hover:border-zinc-600 hover:text-white"
                  }`}
                >
                  {company.ticker}
                </button>
              ))}

              <button
                type="button"
                onClick={() => setShowAllCompanies(!showAllCompanies)}
                className="rounded-full border border-zinc-700 bg-zinc-900 px-4 py-2 text-xs text-zinc-300 transition hover:border-zinc-500 hover:text-white"
              >
                {showAllCompanies ? "− Hide Companies" : "+ More Companies"}
              </button>
            </div>
          </div>

          {/* Additional companies */}
          {showAllCompanies && (
            <div className="mt-6 rounded-2xl border border-zinc-800 bg-zinc-950 p-5">

              <p className="mb-4 text-xs font-medium uppercase tracking-wider text-zinc-500">
                More Companies
              </p>

              <div className="flex flex-wrap justify-center gap-2">
                {additionalCompanies.map((company) => (
                  <button
                    key={company.ticker}
                    type="button"
                    onClick={() => {
                      setTicker(company.ticker);
                      setError("");
                    }}
                    className={`rounded-full border px-4 py-2 text-xs transition ${
                      ticker.toUpperCase() === company.ticker
                        ? "border-zinc-500 bg-zinc-800 text-white"
                        : "border-zinc-800 bg-zinc-900 text-zinc-400 hover:border-zinc-600 hover:text-white"
                    }`}
                  >
                    {company.ticker}
                  </button>
                ))}
              </div>

            </div>
          )}

        </div>

          {/* -------------------------------------------------
              Error
          ------------------------------------------------- */}

          {error && (
            <div className="mt-5 rounded-xl border border-red-900 bg-red-950/40 p-4 text-left text-sm text-red-400">
              {error}
            </div>
          )}

        </section>

        {/* -------------------------------------------------
            FinSight AI Chat
        ------------------------------------------------- */}

        <section className="mt-12 rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
          <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-start">
            <div>
              <p className="text-sm uppercase tracking-wider text-zinc-500">
                FinSight AI
              </p>

              <h3 className="mt-1 text-2xl font-semibold">
                Ask Financial Questions
              </h3>

              <p className="mt-2 max-w-3xl text-sm leading-6 text-zinc-500">
                Ask questions about valuation, earnings, profitability,
                financial health, historical performance, volatility, and risk.
              </p>
            </div>

            <div className="rounded-full border border-zinc-800 px-3 py-1 text-xs text-zinc-500">
              {ticker.trim().toUpperCase() || "No ticker selected"}
            </div>
          </div>

          <form onSubmit={handleChat} className="mt-6">
            <div className="flex flex-col gap-3 sm:flex-row">
              <input
                type="text"
                value={chatQuestion}
                onChange={(event) => setChatQuestion(event.target.value)}
                placeholder={`Ask about ${ticker.trim().toUpperCase() || "a company"}...`}
                className="min-w-0 flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-4 text-white outline-none transition placeholder:text-zinc-600 focus:border-zinc-400"
              />

              <button
                type="submit"
                disabled={chatLoading || !chatQuestion.trim()}
                className="rounded-xl bg-white px-6 py-4 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
              >
                {chatLoading ? "Thinking..." : "Ask FinSight"}
              </button>
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {[
                "What are the main strengths and risks?",
                "How is the company valued?",
                "How has the stock performed historically?",
                "What should I consider before buying?",
                "What is driving the company's earnings growth?",
                "How profitable is the company?",
                "How do trailing and forward EPS compare?",
                "Is the company's financial health strong?",
                "How much debt does the company have?",
                "How volatile has the stock been?",
                "What are the key valuation metrics?",
                "What factors could affect future performance?",
              ].map((question) => (
                <button
                  key={question}
                  type="button"
                  onClick={() => setChatQuestion(question)}
                  className="rounded-full border border-zinc-800 bg-zinc-900 px-3 py-2 text-xs text-zinc-400 transition hover:border-zinc-600 hover:text-white"
                >
                  {question}
                </button>
              ))}
            </div>
          </form>

          {chatError && (
            <div className="mt-5 rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-400">
              {chatError}
            </div>
          )}

          {chatMessages.length > 0 && (
            <div className="mt-6 max-h-[500px] space-y-4 overflow-y-auto rounded-2xl border border-zinc-800 bg-zinc-950 p-4">
              {chatMessages.map((message, index) => (
                <div
                  key={index}
                  className={`flex ${
                    message.role === "user"
                      ? "justify-end"
                      : "justify-start"
                  }`}
                >
                  <div
                    className={`max-w-[85%] rounded-2xl px-4 py-3 ${
                      message.role === "user"
                        ? "bg-blue-600 text-white"
                        : "border border-zinc-800 bg-zinc-900 text-zinc-200"
                    }`}
                  >
                    <p className="mb-1 text-xs font-medium uppercase tracking-wide opacity-60">
                      {message.role === "user" ? "You" : "FinSight AI"}
                    </p>

                    <p className="whitespace-pre-wrap leading-7">
                      {message.content}
                    </p>
                  </div>
                </div>
              ))}
              <div ref={chatEndRef} />
            </div>
          )}

          <p className="mt-5 text-xs leading-5 text-zinc-600">
            FinSight AI provides financial research and decision-support
            information. It does not provide personalized investment advice
            or guarantee future market performance.
          </p>
        </section>

        {/* -------------------------------------------------
            Results
        ------------------------------------------------- */}

        {research && (
          <section className="mt-16 space-y-8">

            {/* -------------------------------------------------
                Company header
            ------------------------------------------------- */}

            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

              <div className="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">

                <div>

                  <p className="text-sm font-medium text-zinc-500">
                    {research.stock_data.ticker}
                  </p>

                  <h3 className="mt-1 text-3xl font-bold">
                    {research.stock_data.company_name ||
                      research.stock_data.ticker}
                  </h3>

                  <p className="mt-2 text-sm text-zinc-500">
                    {research.stock_data.sector || "N/A"} ·{" "}
                    {research.stock_data.industry || "N/A"}
                  </p>

                </div>

                <div className="text-left sm:text-right">

                  <p className="text-sm text-zinc-500">
                    Current Price
                  </p>

                  <p className="text-3xl font-bold">
                    {formatCurrency(
                      research.stock_data.current_price
                    )}
                  </p>

                </div>

              </div>

            </div>

            {/* -------------------------------------------------
                Key financial metrics
            ------------------------------------------------- */}

            <div>

              <h3 className="mb-4 text-xl font-semibold">
                Key Financial Metrics
              </h3>

              <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                <MetricCard
                  label="Market Cap"
                  value={formatLargeNumber(
                    research.stock_data.market_cap
                  )}
                />

                <MetricCard
                  label="Revenue"
                  value={formatLargeNumber(
                    research.stock_data.revenue
                  )}
                />

               <MetricCard
                  label="Net Income"
                  value={formatLargeNumber(
                    research.stock_data.net_income
                  )}
                />

                <MetricCard
                  label="Trailing EPS"
                  value={
                    research.stock_data.trailing_eps !== null
                      ? `$${research.stock_data.trailing_eps.toFixed(2)}`
                      : "N/A"
                  }
                />

                <MetricCard
                  label="Forward EPS"
                  value={
                    research.stock_data.forward_eps !== null
                      ? `$${research.stock_data.forward_eps.toFixed(2)}`
                      : "N/A"
                  }
                />

                <MetricCard
                  label="EPS Growth"
                  value={formatPercent(
                    research.stock_data.eps_growth
                  )}
                />

                <MetricCard
                  label="Profit Margin"
                  value={formatPercent(
                    research.stock_data.profit_margin
                  )}
                />

                <MetricCard
                  label="Operating Margin"
                  value={formatPercent(
                    research.stock_data.operating_margin
                  )}
                />

                <MetricCard
                  label="ROE"
                  value={formatPercent(
                    research.stock_data.return_on_equity
                  )}
                />

                <MetricCard
                  label="Revenue Growth"
                  value={formatPercent(
                    research.stock_data.revenue_growth
                  )}
                />

                <MetricCard
                  label="P/E Ratio"
                  value={
                    research.stock_data.pe_ratio !== null
                      ? research.stock_data.pe_ratio.toFixed(2)
                      : "N/A"
                  }
                />

              </div>

            </div>

            {/* -------------------------------------------------
                Financial Health + Risk
            ------------------------------------------------- */}

            <div className="grid gap-6 lg:grid-cols-2">

              {/* Financial health */}

              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

                <h3 className="text-xl font-semibold">
                  Financial Health
                </h3>

                <div className="mt-4">

                  <HealthBadge
                    label="Profitability"
                    value={
                      research.financial_health.profitability
                    }
                  />

                  <HealthBadge
                    label="Growth"
                    value={research.financial_health.growth}
                  />

                  <HealthBadge
                    label="Capital Efficiency"
                    value={
                      research.financial_health.capital_efficiency
                    }
                  />

                  <HealthBadge
                    label="Liquidity"
                    value={
                      research.financial_health.liquidity
                    }
                  />

                  <HealthBadge
                    label="Leverage"
                    value={
                      research.financial_health.leverage
                    }
                  />

                  <HealthBadge
                    label="Valuation"
                    value={
                      research.financial_health.valuation
                    }
                  />

                  <HealthBadge
                    label="Cash Generation"
                    value={
                      research.financial_health.cash_generation
                    }
                  />

                </div>

              </div>

              {/* Risk */}

              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

                <h3 className="text-xl font-semibold">
                  Risk Analysis
                </h3>

                <div className="mt-6">

                  <p className="text-sm text-zinc-500">
                    Overall Risk Level
                  </p>

                  <p className="mt-2 text-4xl font-bold">
                    {research.risk_analysis.risk_level}
                  </p>

                  <p className="mt-2 text-sm text-zinc-500">
                    Risk Score:{" "}
                    <span className="text-zinc-300">
                      {research.risk_analysis.risk_score}
                    </span>
                  </p>

                </div>

                {research.risk_analysis.risk_flags.length > 0 && (
                  <div className="mt-6">

                    <p className="mb-3 text-sm font-medium text-zinc-400">
                      Risk Flags
                    </p>

                    <div className="space-y-2">

                      {research.risk_analysis.risk_flags.map(
                        (flag, index) => (
                          <div
                            key={index}
                            className="rounded-lg border border-zinc-800 bg-zinc-900 p-3 text-sm text-zinc-400"
                          >
                            {flag}
                          </div>
                        )
                      )}

                    </div>

                  </div>
                )}

              </div>

            </div>

            {/* -------------------------------------------------
                Historical Performance
            ------------------------------------------------- */}

            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

              <h3 className="text-xl font-semibold">
                Historical Performance
              </h3>

              <div className="mt-5 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                <MetricCard
                  label="Revenue CAGR"
                  value={formatPercent(
                    research.historical_analysis.revenue_cagr
                  )}
                  description="Historical revenue growth"
                />

                <MetricCard
                  label="Net Income CAGR"
                  value={formatPercent(
                    research.historical_analysis.net_income_cagr
                  )}
                  description="Historical earnings growth"
                />

                <MetricCard
                  label="5-Year Stock Return"
                  value={formatPercent(
                    research.historical_analysis.stock_return_5y
                  )}
                  description="Historical price performance"
                />

                <MetricCard
                  label="Annualized Volatility"
                  value={formatPercent(
                    research.historical_analysis.annualized_volatility
                  )}
                  description="Historical price volatility"
                />

              </div>

            </div>
            {/* Historical Stock Price Chart */}

            <div className="mt-8">

              <div className="mb-4">
                <h4 className="text-lg font-semibold">
                  Historical Stock Price
                </h4>

                <p className="mt-1 text-sm text-zinc-500">
                  Stock price history over the analyzed period
                </p>
              </div>

              {research.historical_analysis.price_history &&
              research.historical_analysis.price_history.length > 0 ? (
                <div className="h-80 w-full">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart
                      data={research.historical_analysis.price_history}
                      margin={{
                        top: 10,
                        right: 20,
                        left: 10,
                        bottom: 10,
                      }}
                    >
                      <CartesianGrid strokeDasharray="3 3" />

                      <XAxis
                        dataKey="date"
                        tick={{ fontSize: 11 }}
                        tickFormatter={(value) =>
                          new Date(value).toLocaleDateString(
                            "en-US",
                            {
                              month: "short",
                              year: "numeric",
                            }
                          )
                        }
                      />

                      <YAxis
                        tick={{ fontSize: 11 }}
                        domain={["auto", "auto"]}
                      />

                      <Tooltip
                        labelFormatter={(value) =>
                          new Date(String(value)).toLocaleDateString(
                            "en-US",
                            {
                              day: "2-digit",
                              month: "short",
                              year: "numeric",
                            }
                          )
                        }
                        formatter={(value) => [
                          `$${Number(value).toFixed(2)}`,
                          "Close Price",
                        ]}
                      />

                      <Line
                        type="monotone"
                        dataKey="close"
                        strokeWidth={2}
                        dot={false}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              ) : (
                <p className="text-sm text-zinc-500">
                  Historical price data is not available.
                </p>
              )}

            </div>

            {/* -------------------------------------------------
                Market Performance
            ------------------------------------------------- */}

            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

              <div>

                <h3 className="text-xl font-semibold">
                  Market Performance
                </h3>

                <p className="mt-1 text-sm text-zinc-500">
                  Historical stock returns across different time periods
                </p>

                {research.historical_analysis.analysis_date && (
                  <p className="mt-2 text-xs text-zinc-600">
                    Calculated as of{" "}
                    <span className="text-zinc-400">
                      {research.historical_analysis.analysis_date}
                    </span>
                  </p>
                )}

              </div>

              {/* Return cards */}

              <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">

                <MetricCard
                  label="MTD Return"
                  value={formatPercent(
                    marketReturns.mtd_return
                  )}
                  description="Month-to-date"
                />

                <MetricCard
                  label="YTD Return"
                  value={formatPercent(
                    marketReturns.ytd_return
                  )}
                  description="Year-to-date"
                />

                <MetricCard
                  label="3-Month Return"
                  value={formatPercent(
                    marketReturns.three_month_return
                  )}
                  description="Past 3 months"
                />

                <MetricCard
                  label="6-Month Return"
                  value={formatPercent(
                    marketReturns.six_month_return
                  )}
                  description="Past 6 months"
                />

                <MetricCard
                  label="1-Year Return"
                  value={formatPercent(
                    marketReturns.one_year_return
                  )}
                  description="Past 1 year"
                />

                <MetricCard
                  label="3-Year Return"
                  value={formatPercent(
                    marketReturns.three_year_return
                  )}
                  description="Past 3 years"
                />

                <MetricCard
                  label="5-Year Return"
                  value={formatPercent(
                    marketReturns.five_year_return
                  )}
                  description="Past 5 years"
                />

              </div>

              {/* -------------------------------------------------
                  Return chart
              ------------------------------------------------- */}

              <div className="mt-10">

                <h4 className="mb-4 text-sm font-medium text-zinc-400">
                  Return by Period
                </h4>

                <div className="h-[350px] w-full">

                  <ResponsiveContainer
                    width="100%"
                    height="100%"
                  >

                    <BarChart
                      data={marketReturnData}
                      margin={{
                        top: 10,
                        right: 10,
                        left: 0,
                        bottom: 10,
                      }}
                    >

                      <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#27272a"
                      />

                      <XAxis
                        dataKey="period"
                        tick={{
                          fill: "#a1a1aa",
                          fontSize: 12,
                        }}
                        axisLine={{
                          stroke: "#3f3f46",
                        }}
                        tickLine={false}
                      />

                      <YAxis
                        tick={{
                          fill: "#a1a1aa",
                          fontSize: 12,
                        }}
                        axisLine={{
                          stroke: "#3f3f46",
                        }}
                        tickLine={false}
                        tickFormatter={(value) =>
                          `${value}%`
                        }
                      />

                      <Tooltip
                        formatter={(value) => [
                          `${Number(value).toFixed(2)}%`,
                          "Return",
                        ]}
                        contentStyle={{
                          backgroundColor: "#18181b",
                          border: "1px solid #3f3f46",
                          borderRadius: "8px",
                          color: "#fff",
                        }}
                      />

                      <ReferenceLine
                        y={0}
                        stroke="#71717a"
                        strokeWidth={1}
                      />

                      <Bar
                        dataKey="return"
                        radius={[6, 6, 0, 0]}
                      >
                        {marketReturnData.map((entry) => (
                          <Cell
                            key={`cell-${entry.period}`}
                            fill={
                              entry.return >= 0
                                ? "#22c55e"
                                : "#ef4444"
                            }
                          />
                        ))}
                      </Bar>

                    </BarChart>

                  </ResponsiveContainer>

                </div>

              </div>

            </div>

            {/* -------------------------------------------------
                AI Research Report
            ------------------------------------------------- */}

            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">

              <div className="flex items-center justify-between">

                <div>
                  <p className="text-sm uppercase tracking-wider text-zinc-500">
                    AI Analysis
                  </p>

                  <h3 className="mt-1 text-2xl font-semibold">
                    Research Report
                  </h3>

                  <p className="mt-2 text-sm text-zinc-500">
                    Overall AI-generated analysis of the selected company.
                  </p>
                </div>

                <div className="rounded-full border border-zinc-800 px-3 py-1 text-xs text-zinc-500">
                  GPT-powered
                </div>

              </div>

              <div className="mt-6 flex items-center justify-between rounded-xl border border-zinc-800 bg-zinc-900/50 p-4">

                <div>
                  <p className="text-sm font-medium text-zinc-300">
                    Overall Company Analysis
                  </p>

                  <p className="mt-1 text-xs text-zinc-500">
                    View the complete AI-generated research report.
                  </p>
                </div>

                <button
                  type="button"
                  onClick={() => setShowResearchReport(true)}
                  className="rounded-xl bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-zinc-200"
                >
                  View Full Report
                </button>

              </div>

            </div>

          </section>
        )}

      </div>

      {/* -------------------------------------------------
          Overall Research Report Popup
      ------------------------------------------------- */}

      {showResearchReport && research?.ai_report && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 p-4 backdrop-blur-sm"
          onClick={() => setShowResearchReport(false)}
        >
          <div
            className="relative max-h-[85vh] w-full max-w-4xl overflow-hidden rounded-2xl border border-zinc-800 bg-zinc-950 shadow-2xl"
            onClick={(event) => event.stopPropagation()}
          >

            <div className="flex items-center justify-between border-b border-zinc-800 px-6 py-4">

              <div>
                <p className="text-xs uppercase tracking-wider text-zinc-500">
                  FinSight AI
                </p>

                <h3 className="mt-1 text-xl font-semibold text-white">
                  Overall Research Report
                </h3>
              </div>

              <button
                type="button"
                onClick={() => setShowResearchReport(false)}
                className="rounded-lg px-3 py-2 text-zinc-400 transition hover:bg-zinc-800 hover:text-white"
                aria-label="Close research report"
              >
                ✕
              </button>

            </div>

            <div className="max-h-[calc(85vh-80px)] overflow-y-auto px-6 py-6">

              <div className="whitespace-pre-wrap leading-8 text-zinc-300">
                {research.ai_report}
              </div>

            </div>

          </div>
        </div>
      )}

      {/* -------------------------------------------------
          Footer
      ------------------------------------------------- */}

      <footer className="border-t border-zinc-800">

        <div className="mx-auto max-w-7xl px-6 py-8 text-center text-xs text-zinc-600">
          FinSight AI · Financial Intelligence & Research Agent
        </div>

      </footer>
    </main>
  );
}