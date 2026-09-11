const API_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://finsight-ai-financial-intelligence.onrender.com";

export async function researchCompany(ticker: string) {
  const response = await fetch(`${API_URL}/research`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ticker: ticker.trim().toUpperCase(),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Research request failed (${response.status}): ${errorText}`
    );
  }

  return response.json();
}

export async function compareCompanies(tickers: string[]) {
  const response = await fetch(`${API_URL}/compare`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      tickers: tickers.map((ticker) => ticker.trim().toUpperCase()),
    }),
  });

  if (!response.ok) {
    const errorText = await response.text();

    throw new Error(
      `Comparison request failed (${response.status}): ${errorText}`
    );
  }

  return response.json();
}