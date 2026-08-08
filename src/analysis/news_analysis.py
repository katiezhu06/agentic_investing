def calculate_news_score(symbol):

    score = 0

    details = {}

    # Placeholder
    # Later connect News API + LLM


    sentiment_score = 0
    risk_score = 0
    importance_score = 0


    score += sentiment_score
    score += risk_score
    score += importance_score


    details["Sentiment"] = sentiment_score
    details["Risk"] = risk_score
    details["Importance"] = importance_score


    return {
        "news_score": score,
        "details": details
    }


if __name__ == "__main__":

    result = calculate_news_score("AAPL")

    print(result)