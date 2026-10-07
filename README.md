# AI Closing Bell Investment Agent

A Python project that analyzes stocks around market close and produces a structured investment score for **Buy / Hold / Sell decision support**.

This is **not** an autonomous trading system. It does not place trades on its own. The current code collects data, applies heuristic scoring rules, and returns numeric scores that a person (or a later AI explanation layer) can use as decision support.

Repository: [katiezhu06/agentic_investing](https://github.com/katiezhu06/agentic_investing)

---

## Project Overview

The intended workflow is a “Closing Bell” loop: after the market closes, look at a watchlist or portfolio, gather recent market and news data, score each position, and support a Buy / Hold / Sell view with an explanation.

Today, the implemented core is the **data + scoring pipeline**. The LLM explanation layer, portfolio-aware ranking, and full agent workflow are still planned.

The system is designed around multiple signals rather than a single indicator:

- company fundamentals
- short-term technical conditions
- broader market environment
- recent news (sentiment, risk, and importance)
- portfolio fit (planned)

---

## How It Works

Planned architecture:

```text
LLM
 ↓
Financial / MCP Tools
 ↓
Market + Portfolio Data
 ↓
Fundamental + Technical + Market + News + Portfolio Analysis
 ↓
Investment Score
 ↓
Buy / Hold / Sell Decision Support
 ↓
Natural-language Explanation
```

What each stage is meant to do:

| Stage | Role |
| --- | --- |
| **LLM** | Orchestrate the workflow and explain the score in plain language. *Not implemented yet.* |
| **Financial / MCP tools** | Connect to brokerage and market tools (Robinhood MCP is configured; live portfolio fetch is not wired in yet). |
| **Market + portfolio data** | Pull company stats, price history, and news. Watchlist is currently hardcoded. |
| **Analysis modules** | Score fundamentals, technicals, market environment, and news. |
| **Investment score** | Add the implemented component scores into one total. |
| **Decision support** | Use the score as an input to a later Buy / Hold / Sell mapping. *Not implemented yet.* |
| **Explanation** | Turn the numeric result into a readable recommendation. *Not implemented yet.* |

Current execution path in code:

```text
watchlist (AAPL, MSFT, NVDA, META, AMZN)
 ↓
market data (yfinance) + company news (Finnhub)
 ↓
fundamental + technical + market + news scores
 ↓
integrated investment score (max 80 today)
```

Run the pipeline with:

```bash
python src/main.py
```

Or score one symbol:

```bash
python -m src.analysis.investment_score
```

---

## Investment Scoring Framework

The **planned** framework is 100 points:

| Category | Points | Status |
| --- | ---: | --- |
| Fundamental Analysis | 30 | Implemented |
| Technical Analysis | 20 | Implemented |
| Market Environment | 10 | Implemented |
| News Sentiment | 20 | Implemented |
| Portfolio Fit | 20 | Not implemented |
| **Total** | **100** | **80 points wired in today** |

The 100-point ranking system, Buy / Hold / Sell mapping, and AI-generated explanation are **not** complete. `investment_score.py` currently adds the four implemented modules.

---

## Fundamental Analysis

File: `src/analysis/fundamental_analysis.py`

Data comes from the market data layer (`src/data/market_data.py`, via yfinance): ROE, profit margin, trailing P/E, and trailing EPS.

Current 30-point framework (maximums used in code):

| Metric | Max points | What it is meant to capture |
| --- | ---: | --- |
| ROE | 8 | How effectively the company uses equity |
| Profit Margin | 8 | Profitability |
| P/E Ratio | 7 | Valuation (mid-range P/E scores higher than very expensive or weak readings) |
| EPS | 7 | Earnings level |

Higher is better within these heuristic buckets. The rules are simple thresholds, not a valuation model.

---

## Technical Analysis

File: `src/analysis/technical_analysis.py`

Uses 6 months of daily price history. The technical category is **20 points** in the overall framework. The current implementation uses three signals:

| Signal | Current points in code | What it is meant to measure |
| --- | --- | --- |
| 20-day moving average | 7 if price is above MA20, otherwise 3 | Short-term trend: is the stock trading above its recent average? |
| RSI (14-day) | 8 / 7 / 6 / 3 depending on the RSI zone | Momentum: oversold, mid-range, or overbought |
| Volume ratio | 5 / 3 / 1 vs. 20-day average volume | Whether recent trading activity is elevated |

These buckets currently add up to a maximum of 20. They are heuristic, not a trading strategy.

---

## Market Environment

File: `src/analysis/market_analysis.py`

This score is a **general market-condition signal**, not a stock-specific forecast. The same market score is applied regardless of which ticker is being evaluated.

It currently uses:

- S&P 500 (`^GSPC`)
- Nasdaq-100 ETF (`QQQ`)

For each index/ETF, the latest close is compared with its 20-day moving average:

- above MA20 → 5 points, labeled bullish
- below MA20 → 2 points, labeled bearish

Maximum: **10 points**.

---

## News Analysis

Files:

- `src/data/news_data.py` — fetch and filter Finnhub company news
- `src/analysis/news_analysis.py` — score articles and aggregate a news score

This is a **keyword-based baseline**. It does **not** call an LLM for sentiment.

### Pipeline

```text
Finnhub company-news
 ↓
Relevance filtering
 ↓
Article-level analysis
 ↓
Sentiment + Risk + Importance
 ↓
Weighted aggregation
 ↓
News Score / 20
```

`get_company_news(symbol)` calls Finnhub’s company-news endpoint for roughly the last 7 days, keeps articles with a headline and summary, drops duplicates, and keeps articles that mention the target company (name, products, or similar keywords).

### Relevance

Articles are labeled, not simply dropped:

- **Direct** — company keywords appear in the headline; the story is mainly about the target company.
- **Related** — company keywords appear in the summary, or the story looks like industry/competitor context that could still affect the stock.
- **Unknown** — weak connection. The scorer may still treat it as related if industry-impact language is present.

Related news is kept on purpose. A story about Microsoft, Google, Amazon, Samsung, semiconductors, AI, tariffs, or regulation can move another technology stock even if that stock is not the headline. Direct articles get more weight; related articles get less weight; they are not ignored.

### Article-level scores

| Component | Range | Role |
| --- | --- | --- |
| Sentiment | 0–10 | Positive language raises the score; negative language lowers it. Neutral starts at 5. |
| Risk | 0–5 | Legal, regulatory, operational, or similar risk language. |
| Importance | 0–5 | Larger events (earnings, deals, product launches) score higher than minor mentions. |

Scoring uses keyword lists on the headline and summary.

### Aggregation

Each article is weighted by relevance, then averaged:

- direct: weight `1.0`
- related: weight `0.6`
- unknown: weight `0.4`

### Investment interpretation of risk

Higher risk **must not** increase the investment score.

```text
News Score = Sentiment + Importance - Risk
```

The result is clamped to **0–20**.

Example from a recent AAPL run:

```text
Sentiment  = 6
Importance = 3
Risk       = 0
News Score = 6 + 3 - 0 = 9 / 20
```

Later versions could replace this keyword baseline with LLM-based semantic sentiment and risk analysis.

---

## Investment Score Integration

File: `src/analysis/investment_score.py`

`calculate_investment_score(symbol)` currently combines:

```text
Fundamental / 30
Technical    / 20
Market       / 10
News         / 20
────────────────
Total        / 80
```

Portfolio Fit (/20) is planned and is **not** included.

Example from a recent `python -m src.analysis.investment_score` run on AAPL (live data, so numbers will change):

```text
Fundamental: 26/30
Technical:   15/20
Market:      10/10
News:         9/20
Total:       60/80
```

The returned dictionary includes each component object, so the news score and its details (sentiment, risk, importance, articles analyzed) are visible in the output.

---

## Project Structure

```text
agentic_investing/
├── src/
│   ├── main.py
│   ├── data/
│   │   ├── market_data.py      # yfinance company stats and price history
│   │   ├── news_data.py        # Finnhub fetch + relevance helpers
│   │   ├── watchlist.py        # current hardcoded ticker list
│   │   └── portfolio_data.py   # placeholder for later portfolio fetch
│   └── analysis/
│       ├── fundamental_analysis.py
│       ├── technical_analysis.py
│       ├── market_analysis.py
│       ├── news_analysis.py
│       └── investment_score.py
├── .cursor/
│   └── mcp.json                # Robinhood MCP endpoint
├── .gitignore
├── README.md
├── config.py                   # placeholder
└── requirments.txt
```

Empty folders such as `src/ai`, `src/portfolio`, `src/utils`, and `tests` exist as placeholders and do not contain code yet.

---

## Tech Stack

Used in the current codebase:

- Python
- yfinance
- pandas (price history, moving averages, RSI, volume)
- requests
- python-dotenv
- Finnhub API (company news)
- Robinhood MCP config (`.cursor/mcp.json`) for a later brokerage connection

Not used in the scoring code yet: LLM APIs, live Robinhood portfolio/order tools.

---

## Setup

1. Clone the repository:

```bash
git clone https://github.com/katiezhu06/agentic_investing.git
cd agentic_investing
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
```

3. Install packages:

```bash
pip install yfinance pandas requests python-dotenv
```

4. Add a Finnhub API key in a local `.env` file (this file is gitignored):

```bash
FINNHUB_API_KEY=your_key_here
```

News scoring needs that key. Market/fundamental/technical scoring uses yfinance and does not require Finnhub.

---

## Current Progress

**Completed**

- [x] Market data layer (yfinance)
- [x] Watchlist of sample tickers
- [x] Fundamental analysis
- [x] Technical analysis (moving average, RSI, volume ratio)
- [x] Market environment (S&P 500 and QQQ vs. 20-day MA)
- [x] News data retrieval (Finnhub)
- [x] News relevance filtering (direct / related / unknown)
- [x] News sentiment, risk, and importance scoring
- [x] Investment score integration of the implemented components (max 80)

**Planned**

- [ ] Portfolio Fit (/20)
- [ ] Stock ranking across a portfolio
- [ ] Full 100-point final scoring
- [ ] Buy / Hold / Sell mapping
- [ ] AI-generated investment explanation
- [ ] Full Closing Bell agent workflow (LLM + MCP tools)
- [ ] Live watchlist/portfolio from Robinhood MCP

---

## Limitations / Future Improvements

- Keyword-based news analysis is a baseline. It can miss sarcasm, context, or mixed articles, and it can over-count generic words.
- Market and news data depend on external APIs (yfinance, Finnhub). Missing data or API errors reduce coverage; empty news returns a news score of 0.
- Scoring rules are heuristics, not a statistically validated investment model. They are for coursework and prototyping, not production research.
- The market environment score is shared across all tickers; it does not measure a stock’s beta or sector relative strength.
- This project provides **decision support**, not financial advice, and it is not a licensed or autonomous trading system.
- Future work: LLM-based news analysis, portfolio-aware scoring, clearer Buy/Hold/Sell thresholds, and an explanation layer that cites the component scores.

---

## Author

Katie Zhu
