from src.data.market_data import get_price_history



def calculate_market_score():

    score = 0

    details = {}


    # =====================
    # S&P500
    # =====================
    sp500 = get_price_history("^GSPC")

    sp500_close = sp500["Close"]

    sp500_ma20 = sp500_close.rolling(window=20).mean().iloc[-1]

    sp500_current = sp500_close.iloc[-1]

    sp500_ratio = sp500_current / sp500_ma20


    if sp500_current > sp500_ma20:
        sp500_score = 5
        sp500_trend = "bullish"
    else:
        sp500_score = 2
        sp500_trend = "bearish"


    score += sp500_score

    details["S&P500"] = {
        "score": sp500_score,
        "price_to_ma20_ratio": float(sp500_ratio),
    "trend": sp500_trend
}


    # =====================
    # QQQ
    # =====================

    qqq = get_price_history("QQQ")

    qqq_close = qqq["Close"]

    qqq_ma20 = qqq_close.rolling(window=20).mean().iloc[-1]

    qqq_current = qqq_close.iloc[-1]

    qqq_ratio = qqq_current / qqq_ma20


    if qqq_current > qqq_ma20:
        qqq_score = 5
        qqq_trend = "bullish"
    else:
        qqq_score = 2
        qqq_trend = "bearish"


    score += qqq_score

    details["QQQ"] = {
        "score": qqq_score,
        "price_to_ma20_ratio": float(qqq_ratio),
        "trend": qqq_trend
}


    return {
        "market_score": score,
        "details": details
    }



if __name__ == "__main__":

    result = calculate_market_score()

    print(result)