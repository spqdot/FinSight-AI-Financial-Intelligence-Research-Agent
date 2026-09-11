"use client";

import { FormEvent, useState } from "react";
import MetricCard from "@/components/MetricCard";
import HealthBadge from "@/components/HealthBadge";
import { researchCompany } from "@/lib/api";

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
    revenue_growth: number | null;
    earnings_growth: number | null;
    pe_ratio: number | null;
    forward_pe: number | null;
    price_to_book: number | null;
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
    revenue_cagr: number | null;
    net_income_cagr: number | null;
    five_year_stock_return: number | null;
    annualized_volatility: number | null;
  };
  risk_analysis: {
    risk_level: string;
    risk_score: number;
    risk_flags: string[];
  };
  ai_report: string;
}

function formatCurrency(value: number | null) {
  if (value === null || value === undefined) return "N/A";

  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 2,
  }).format(value);
}

function formatLargeNumber(value: number | null) {
  if (value === null || value === undefined) return "N/A";

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
  if (value === null || value === undefined) return "N/A";

  return `${(value * 100).toFixed(1)}%`;
}

export default function Home() {
  const [ticker, setTicker] = useState("MSFT");
  const [research, setResearch] = useState<ResearchData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleResearch(event: FormEvent) {
    event.preventDefault();

    if (!ticker.trim()) return;

    setLoading(true);
    setError("");
    setResearch(null);

    try {
      const data = await researchCompany(ticker);
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

  return (
    <main className="min-h-screen bg-black text-white">
      {/* Header */}
      <header className="border-b border-zinc-800">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-xl font-bold tracking-tight">
              FinSight <span className="text-zinc-500">AI</span>
            </h1>
            <p className="text-xs text-zinc-500">
              Financial Intelligence & Research Agent
            </p>
          </div>

          <div className="rounded-full border border-zinc-800 px-4 py-2 text-xs text-zinc-400">
            AI Financial Research
          </div>
        </div>
      </header>

      <div className="mx-auto max-w-7xl px-6 py-12">
        {/* Hero */}
        <section className="mx-auto max-w-3xl text-center">
          <p className="mb-4 text-sm font-medium uppercase tracking-[0.25em] text-zinc-500">
            Financial Intelligence
          </p>

          <h2 className="text-4xl font-bold tracking-tight sm:text-5xl">
            Analyze a company with AI
          </h2>

          <p className="mt-5 text-lg leading-8 text-zinc-400">
            Get financial metrics, historical performance, risk analysis,
            and an AI-generated research report from one place.
          </p>

          {/* Search */}
          <form
            onSubmit={handleResearch}
            className="mx-auto mt-8 flex max-w-2xl gap-3"
          >
            <input
              type="text"
              value={ticker}
              onChange={(event) => setTicker(event.target.value)}
              placeholder="Enter ticker e.g. MSFT"
              className="min-w-0 flex-1 rounded-xl border border-zinc-700 bg-zinc-900 px-5 py-4 text-white outline-none transition focus:border-zinc-400"
            />

            <button
              type="submit"
              disabled={loading}
              className="rounded-xl bg-white px-6 py-4 font-semibold text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading ? "Analyzing..." : "Analyze"}
            </button>
          </form>

          {error && (
            <div className="mt-5 rounded-xl border border-red-900 bg-red-950/40 p-4 text-left text-sm text-red-400">
              {error}
            </div>
          )}
        </section>

        {/* Results */}
        {research && (
          <section className="mt-16 space-y-8">
            {/* Company header */}
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
                  <p className="text-sm text-zinc-500">Current Price</p>
                  <p className="text-3xl font-bold">
                    {formatCurrency(
                      research.stock_data.current_price
                    )}
                  </p>
                </div>
              </div>
            </div>

            {/* Key metrics */}
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

            {/* Financial health */}
            <div className="grid gap-6 lg:grid-cols-2">
              <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
                <h3 className="text-xl font-semibold">
                  Financial Health
                </h3>

                <div className="mt-4">
                  <HealthBadge
                    label="Profitability"
                    value={research.financial_health.profitability}
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
                    value={research.financial_health.liquidity}
                  />

                  <HealthBadge
                    label="Leverage"
                    value={research.financial_health.leverage}
                  />

                  <HealthBadge
                    label="Valuation"
                    value={research.financial_health.valuation}
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

            {/* Historical analysis */}
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
                    research.historical_analysis
                      .five_year_stock_return
                  )}
                  description="Historical price performance"
                />

                <MetricCard
                  label="Annualized Volatility"
                  value={formatPercent(
                    research.historical_analysis
                      .annualized_volatility
                  )}
                  description="Historical price volatility"
                />
              </div>
            </div>

            {/* AI Report */}
            <div className="rounded-2xl border border-zinc-800 bg-zinc-950 p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm uppercase tracking-wider text-zinc-500">
                    AI Analysis
                  </p>

                  <h3 className="mt-1 text-2xl font-semibold">
                    Research Report
                  </h3>
                </div>

                <div className="rounded-full border border-zinc-800 px-3 py-1 text-xs text-zinc-500">
                  GPT-powered
                </div>
              </div>

              <div className="mt-6 whitespace-pre-wrap leading-8 text-zinc-300">
                {research.ai_report}
              </div>
            </div>
          </section>
        )}
      </div>

      {/* Footer */}
      <footer className="border-t border-zinc-800">
        <div className="mx-auto max-w-7xl px-6 py-8 text-center text-xs text-zinc-600">
          FinSight AI · Financial Intelligence & Research Agent
        </div>
      </footer>
    </main>
  );
}