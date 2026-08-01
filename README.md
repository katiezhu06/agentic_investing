Agentic Investing

An AI-powered investment analysis agent that evaluates stock holdings using fundamental analysis, technical indicators, market data, and LLM-based reasoning.

The goal of this project is to build an intelligent investment assistant that analyzes portfolio positions near market close and provides explainable investment insights.

⸻

Project Overview

The AI Closing Bell Investment Agent follows this workflow:

Market Close
      |
      ↓
Retrieve Portfolio Data
      |
      ↓
Collect Market Data
      |
      ↓
Fundamental Analysis
      |
      ↓
Technical Analysis
      |
      ↓
Investment Score Generation
      |
      ↓
AI Explanation & Recommendation

The system evaluates stocks based on multiple dimensions:

* Fundamental strength
* Technical momentum
* Trading activity
* Market conditions
* Portfolio fit

⸻

Features

1. Fundamental Analysis

The fundamental analysis module evaluates company financial health using:

Metric	Description
ROE	Return on Equity
Profit Margin	Company profitability
PE Ratio	Valuation measurement
EPS	Earnings performance

Example output:

{
    "fundamental_score": 26,
    "details": {
        "ROE": 7,
        "Profit Margin": 8,
        "PE Ratio": 4,
        "EPS": 7
    }
}

⸻

2. Technical Analysis

The technical analysis module currently includes:

Moving Average

Compares current price with the 20-day moving average.

Purpose:

* Identify short-term price trends
* Determine whether price momentum is positive or negative

RSI (Relative Strength Index)

Measures recent price momentum.

The RSI score evaluates whether a stock is:

* Oversold
* Neutral
* Overbought

Volume Ratio

Measures current trading volume compared with the average volume.

Formula:

Volume Ratio = Current Volume / Average Volume(20 days)

Higher volume may indicate stronger market interest.

⸻

Example output:

{
    "technical_score": 16,
    "details": {
        "Moving Average": 7,
        "RSI": 8,
        "Volume Score": 1
    }
}

⸻

Investment Score Framework

The final investment score combines multiple categories:

Category	Weight
Fundamental Analysis	30
Technical Analysis	20
News Sentiment	20
Market Environment	10
Portfolio Fit	20
Total	100

⸻

Project Structure

agentic_investing/
│
├── src/
│   ├── main.py
│   │
│   ├── data/
│   │   ├── market_data.py
│   │   ├── news_data.py
│   │   └── portfolio_data.py
│   │
│   ├── analysis/
│   │   ├── fundamental_analysis.py
│   │   └── technical_analysis.py
│
├── README.md
├── requirements.txt
└── .gitignore

⸻

Installation

Clone the repository:

git clone https://github.com/katiezhu06/agentic_investing.git

Create virtual environment:

python -m venv .venv

Activate environment:

Mac/Linux:

source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt

⸻

Running the Project

Run:

python src/main.py

Example:

Checking: AAPL
Fundamental:
{
    "fundamental_score": 26
}
Technical:
{
    "technical_score": 16
}

⸻

Development Roadmap

Completed

* Connect market data API
* Fundamental analysis module
* Moving Average indicator
* RSI indicator
* Volume Ratio indicator
* Technical scoring system

In Progress

* Momentum indicators
* News sentiment analysis
* Market environment analysis
* Portfolio risk analysis
* LLM investment explanation module

⸻

Technologies

* Python
* Pandas
* NumPy
* yfinance
* Git/GitHub
* Model Context Protocol (MCP)
* Large Language Models (LLMs)

⸻

Author

Katie Zhu