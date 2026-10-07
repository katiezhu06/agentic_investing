import os
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv


load_dotenv()

COMPANY_NAMES = {
    "AAPL": [
        "apple",
        "iphone",
        "ipad",
        "mac",
        "app store",
        "tim cook"
    ],
    "MSFT": [
        "microsoft",
        "windows",
        "azure",
        "copilot",
        "satya nadella"
    ],
    "NVDA": [
        "nvidia",
        "geforce",
        "cuda",
        "jensen huang"
    ],
    "META": [
        "meta",
        "facebook",
        "instagram",
        "whatsapp",
        "zuckerberg"
    ],
    "AMZN": [
        "amazon",
        "aws",
        "prime",
        "andy jassy"
    ],
}

def is_relevant_article(article, symbol):
    headline = article.get("headline", "")
    summary = article.get("summary", "")

    text = f"{headline} {summary}".lower()

    company_keywords = COMPANY_NAMES.get(symbol.upper(), [])

    return any(
        keyword in text
        for keyword in company_keywords
    )

def get_relevance_type(article, symbol):
    headline = article.get("headline", "")
    summary = article.get("summary", "")

    text = f"{headline} {summary}".lower()

    company_keywords = COMPANY_NAMES.get(symbol.upper(), [])

    for keyword in company_keywords:
        if keyword in headline.lower():
            return "direct"

    for keyword in company_keywords:
        if keyword in summary.lower():
            return "related"

    return "unknown"
    
def get_date_range(days=7):
    """
    Return the date range for the most recent `days` days.
    """

    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    return (
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )


def get_company_news(symbol, days=7, max_articles=20):
    """
    Fetch and clean recent company news from Finnhub.

    Args:
        symbol: Stock ticker symbol, such as AAPL or NVDA.
        days: Number of recent days to retrieve.

    Returns:
        A list of cleaned news articles.
    """

    api_key = os.getenv("FINNHUB_API_KEY")

    if not api_key:
        print("Error: FINNHUB_API_KEY not found.")
        return []

    from_date, to_date = get_date_range(days)

    url = "https://finnhub.io/api/v1/company-news"

    params = {
        "symbol": symbol,
        "from": from_date,
        "to": to_date,
        "token": api_key
    }

    try:
        response = requests.get(url, params=params, timeout=10)

    except requests.RequestException as error:
        print(f"Error fetching news for {symbol}: {error}")
        return []

    if response.status_code != 200:
        print(f"Status code for {symbol}: {response.status_code}")
        print("Response:", response.text)
        return []

    articles = response.json()

    cleaned_news = []
    seen = set()

    for article in articles:

        headline = article.get("headline")
        summary = article.get("summary")

        if not is_relevant_article(article, symbol):
            continue

        # Skip articles without essential information
        if not headline or not summary:
            continue

        url = article.get("url")

        # Use headline + URL to identify duplicate articles
        article_id = (headline, url)

        if article_id in seen:
            continue

        seen.add(article_id)

        cleaned_news.append({
            "headline": headline,
            "summary": summary,
            "source": article.get("source"),
            "datetime": article.get("datetime"),
            "url": url
        })

    cleaned_news.sort(
        key=lambda article: article.get("datetime", 0),
        reverse=True
)

    return cleaned_news[:max_articles]


def get_news_for_stocks(symbols, days=7):
    """
    Fetch news for multiple stocks.

    Returns:
        Dictionary mapping each stock symbol to its news articles.
    """

    all_news = {}

    for symbol in symbols:
        all_news[symbol] = get_company_news(symbol, days)

    return all_news


if __name__ == "__main__":

    symbols = ["AAPL", "MSFT", "NVDA", "META", "AMZN"]

    all_news = get_news_for_stocks(symbols)

    for symbol, news in all_news.items():

        print(f"\n{symbol}: {len(news)} news articles")

        for article in news[:3]:
            print("-", article["headline"])