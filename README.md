# AI Closing Bell Investment Agent

## Project Goal

Build an AI-powered end-of-day trading agent that analyzes stocks near the market close (e.g., 3:45 PM ET), evaluates company fundamentals, technical indicators, news sentiment, and overall market conditions, then generates a trading score and recommends whether to **Buy**, **Hold**, or **Sell**.

For existing positions, the agent also evaluates whether exit conditions have been met. If the user approves, the agent prepares a Robinhood order for review through the Robinhood MCP.

Unlike a simple rule-based trading bot, this project focuses on AI reasoning, explainability, and decision support.

---

# Current Progress

## ✅ Completed

### Data Module

- Retrieve stock fundamental data using Yahoo Finance
- Retrieve historical price data (6 months)
- Support multiple stocks through a customizable watchlist

### Fundamental Analysis

Implemented a rule-based scoring system using:

- Return on Equity (ROE)
- Profit Margin
- Price-to-Earnings (P/E) Ratio
- Earnings Per Share (EPS)

Current Score: **35 points**

---

### Technical Analysis

Implemented:

- ✅ 20-Day Moving Average (MA20)

Planned:

- RSI
- Trading Volume
- Price Momentum

Current Score: **7 / 25 points implemented**

---

# Workflow

```text
Watchlist
      │
      ▼
Retrieve Stock Data
      │
      ▼
Retrieve Price History
      │
      ▼
Fundamental Analysis
      │
      ▼
Technical Analysis
      │
      ▼
News Sentiment (Planned)
      │
      ▼
Market Environment (Planned)
      │
      ▼
Generate Trading Score
      │
      ▼
LLM Investment Reasoning
      │
      ▼
Buy / Hold / Sell Recommendation
      │
      ▼
(Optional)
Prepare Robinhood Order
```

---

# Project Structure

```text
agentic_investing/

src/
│
├── main.py
│
├── data/
│   ├── market_data.py
│   ├── watchlist.py
│   ├── news_data.py
│   └── portfolio_data.py
│
└── analysis/
    ├── fundamental_analysis.py
    └── technical_analysis.py
```

---

# Scoring System

## Fundamental Analysis (35 pts)

| Metric | Points |
|--------|-------:|
| ROE | 7 |
| Profit Margin | 8 |
| P/E Ratio | 10 |
| EPS | 10 |

---

## Technical Analysis (25 pts)

| Metric | Points | Status |
|--------|-------:|--------|
| Moving Average | 7 | ✅ Completed |
| RSI | 8 | 🚧 Planned |
| Volume | 5 | 🚧 Planned |
| Momentum | 5 | 🚧 Planned |

---

## News Sentiment (20 pts)

Planned features:

- News collection
- LLM sentiment analysis
- Business impact evaluation
- Confidence score

---

## Market Environment (15 pts)

Planned features:

- S&P 500 daily performance
- QQQ daily performance

---

# Technologies

- Python
- pandas
- yfinance
- Git
- GitHub

Future:

- OpenAI API
- Robinhood MCP
- News API
- LangGraph