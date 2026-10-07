from src.data.news_data import get_company_news, get_relevance_type


# Words that usually mean the news is good for the stock.
POSITIVE_WORDS = [
    "beat",
    "beats",
    "beating",
    "growth",
    "record",
    "profit",
    "profitable",
    "upgrade",
    "upgraded",
    "outperform",
    "surge",
    "rally",
    "gain",
    "gains",
    "soar",
    "soars",
    "jump",
    "jumps",
    "partnership",
    "deal",
    "launch",
    "launches",
    "innovation",
    "strong",
    "bullish",
    "expansion",
    "dividend",
    "buyback",
    "approval",
    "approved",
    "win",
    "wins",
    "contract",
    "optimistic",
    "all-time high",
    "revenue growth",
]


# Words that usually mean the news is bad for the stock.
NEGATIVE_WORDS = [
    "miss",
    "misses",
    "missed",
    "decline",
    "drop",
    "drops",
    "fall",
    "falls",
    "loss",
    "losses",
    "lawsuit",
    "layoff",
    "layoffs",
    "downgrade",
    "downgraded",
    "weak",
    "bearish",
    "warning",
    "cut",
    "cuts",
    "delay",
    "delayed",
    "recall",
    "scandal",
    "fraud",
    "investigation",
    "fine",
    "penalty",
    "crash",
    "plunge",
    "slump",
    "underperform",
    "bankruptcy",
    "disappointing",
    "slowdown",
]


# Words that point to legal, regulatory, or operational risk.
RISK_WORDS = [
    "lawsuit",
    "litigation",
    "investigation",
    "probe",
    "recall",
    "hack",
    "breach",
    "cybersecurity",
    "regulation",
    "regulatory",
    "antitrust",
    "ban",
    "banned",
    "tariff",
    "tariffs",
    "fine",
    "penalty",
    "sec",
    "ftc",
    "doj",
    "default",
    "bankruptcy",
    "layoff",
    "layoffs",
    "strike",
    "shortage",
    "recession",
    "sanction",
    "sanctions",
    "outage",
    "data leak",
    "privacy",
    "class action",
    "guidance cut",
]


# Company-level events that usually matter a lot to investors.
HIGH_IMPORTANCE_WORDS = [
    "earnings",
    "guidance",
    "acquisition",
    "merger",
    "takeover",
    "ceo",
    "product launch",
    "dividend",
    "buyback",
    "stock split",
    "approval",
    "antitrust",
    "quarterly results",
    "revenue",
    "forecast",
]


# Useful but smaller events.
MEDIUM_IMPORTANCE_WORDS = [
    "analyst",
    "upgrade",
    "downgrade",
    "partnership",
    "contract",
    "expansion",
    "hiring",
    "layoff",
    "price target",
    "rating",
    "launch",
]


# Industry or competitor language that can still move the target stock.
INDUSTRY_IMPACT_WORDS = [
    "competitor",
    "competitors",
    "industry",
    "sector",
    "samsung",
    "google",
    "alphabet",
    "microsoft",
    "amazon",
    "tesla",
    "intel",
    "tsmc",
    "semiconductor",
    "smartphone",
    "supply chain",
    "chip",
    "chips",
    "tariff",
    "tariffs",
    "regulation",
    "antitrust",
    "ai",
    "consumer spending",
]


def count_keyword_hits(text, keywords):
    """
    Count how many keywords from the list appear in the text.
    Each keyword is counted at most once.
    """

    hits = 0

    for word in keywords:
        if word in text:
            hits += 1

    return hits


def clamp(value, minimum, maximum):
    """Keep a number inside a min/max range."""

    return max(minimum, min(maximum, value))


def classify_relevance(article, symbol):
    """
    Decide if the article is directly about the target company
    or related news that could still affect the stock.

    We do not drop related news. We only label it so we can
    give it a smaller weight later.
    """

    relevance = get_relevance_type(article, symbol)

    headline = article.get("headline", "")
    summary = article.get("summary", "")
    text = f"{headline} {summary}".lower()

    # If the company filter did not mark it as direct/related,
    # still keep it when the story looks like industry impact.
    if relevance == "unknown":
        if count_keyword_hits(text, INDUSTRY_IMPACT_WORDS) > 0:
            relevance = "related"

    return relevance


def score_article(article, symbol):
    """
    Score one article using the headline and summary.

    Returns:
        sentiment 0-10
        risk 0-5
        importance 0-5
        relevance label
    """

    headline = article.get("headline", "")
    summary = article.get("summary", "")
    text = f"{headline} {summary}".lower()

    relevance = classify_relevance(article, symbol)

    # Related news can still matter, but usually less than
    # news that is clearly about the target company.
    if relevance == "direct":
        impact_weight = 1.0
    elif relevance == "related":
        impact_weight = 0.6
    else:
        impact_weight = 0.4


    # -------------------------
    # Sentiment (0-10)
    # Start at 5 (neutral), then move up or down.
    # -------------------------

    positive_hits = count_keyword_hits(text, POSITIVE_WORDS)
    negative_hits = count_keyword_hits(text, NEGATIVE_WORDS)

    sentiment_shift = min(positive_hits, 5) - min(negative_hits, 5)
    sentiment = 5 + (sentiment_shift * impact_weight)
    sentiment = int(round(clamp(sentiment, 0, 10)))


    # -------------------------
    # Risk (0-5)
    # Risk words raise the score. Industry risk still counts,
    # because regulation or tariffs can affect the target stock.
    # -------------------------

    risk_hits = count_keyword_hits(text, RISK_WORDS)
    risk = min(risk_hits, 5)

    # Related news can still raise risk, just a little less.
    if relevance != "direct":
        risk = int(round(risk * impact_weight))

    risk = int(clamp(risk, 0, 5))


    # -------------------------
    # Importance (0-5)
    # Bigger company/industry events get a higher score.
    # -------------------------

    importance = 1

    high_hits = count_keyword_hits(text, HIGH_IMPORTANCE_WORDS)
    medium_hits = count_keyword_hits(text, MEDIUM_IMPORTANCE_WORDS)

    if high_hits >= 2:
        importance += 3
    elif high_hits == 1:
        importance += 2

    if medium_hits >= 2:
        importance += 2
    elif medium_hits == 1:
        importance += 1

    if relevance == "direct":
        importance += 1

    importance = int(round(importance * impact_weight))
    importance = int(clamp(importance, 0, 5))


    return {
        "headline": headline,
        "relevance": relevance,
        "Sentiment": sentiment,
        "Risk": risk,
        "Importance": importance,
    }


def calculate_news_score(symbol):
    """
    Fetch recent news for a stock and turn it into one news score.

    The total score is out of 20:
        Sentiment (0-10) + Importance (0-5) - Risk (0-5)
    """

    news = get_company_news(symbol)

    # No news should return a score of 0 without crashing.
    if not news:
        return {
            "news_score": 0,
            "details": {
                "Sentiment": 0,
                "Risk": 0,
                "Importance": 0,
            },
            "articles_analyzed": 0,
        }


    article_scores = []

    for article in news:
        article_scores.append(score_article(article, symbol))


    # Weighted average: direct articles count more than related ones.
    total_weight = 0.0
    sentiment_total = 0.0
    risk_total = 0.0
    importance_total = 0.0

    for item in article_scores:
        if item["relevance"] == "direct":
            weight = 1.0
        elif item["relevance"] == "related":
            weight = 0.6
        else:
            weight = 0.4

        total_weight += weight
        sentiment_total += item["Sentiment"] * weight
        risk_total += item["Risk"] * weight
        importance_total += item["Importance"] * weight


    if total_weight == 0:
        sentiment_score = 0
        risk_score = 0
        importance_score = 0
    else:
        sentiment_score = int(round(clamp(sentiment_total / total_weight, 0, 10)))
        risk_score = int(round(clamp(risk_total / total_weight, 0, 5)))
        importance_score = int(round(clamp(importance_total / total_weight, 0, 5)))


    total_score = sentiment_score + importance_score - risk_score
    total_score = int(clamp(total_score, 0, 20))


    return {
        "news_score": total_score,
        "details": {
            "Sentiment": sentiment_score,
            "Risk": risk_score,
            "Importance": importance_score,
        },
        "articles_analyzed": len(article_scores),
    }



if __name__ == "__main__":

    symbol = "AAPL"

    result = calculate_news_score(symbol)

    print("News score:", result["news_score"])
    print("Sentiment score:", result["details"]["Sentiment"])
    print("Risk score:", result["details"]["Risk"])
    print("Importance score:", result["details"]["Importance"])
    print("Number of articles analyzed:", result["articles_analyzed"])

    print("\nFirst 3 articles:")

    news = get_company_news(symbol)

    for article in news[:3]:
        scored = score_article(article, symbol)

        print("-", scored["headline"])
        print("  relevance:", scored["relevance"])
        print("  sentiment:", scored["Sentiment"])
        print("  risk:", scored["Risk"])
        print("  importance:", scored["Importance"])
