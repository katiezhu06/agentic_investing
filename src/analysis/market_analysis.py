from data.market_data import get_market_history


def calculate_market_score():

    score = 0

    details = {}


    # =====================
    # S&P500
    # =====================

    sp500 = get_market_history("^GSPC")

    sp500_close = sp500["Close"]

    sp500_ma20 = sp500_close.rolling(window=20).mean().iloc[-1]

    sp500_current = sp500_close.iloc[-1]

    sp500_ratio = sp500_current / sp500_ma20


    if sp500_current > sp500_ma20:
        sp500_score = 5
    else:
        sp500_score = 2


    score += sp500_score

    details["S&P500"] = {
        "score": sp500_score,
        "ratio": sp500_ratio
    }



    # =====================
    # QQQ
    # =====================

    qqq = get_market_history("QQQ")

    qqq_close = qqq["Close"]

    qqq_ma20 = qqq_close.rolling(window=20).mean().iloc[-1]

    qqq_current = qqq_close.iloc[-1]

    qqq_ratio = qqq_current / qqq_ma20


    if qqq_current > qqq_ma20:
        qqq_score = 5
    else:
        qqq_score = 2


    score += qqq_score

    details["QQQ"] = {
        "score": qqq_score,
        "ratio": qqq_ratio
    }


    return {
        "market_score": score,
        "details": details
    }



if __name__ == "__main__":

    result = calculate_market_score()

    print(result)