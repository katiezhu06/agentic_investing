def calculate_technical_score(price_history):

    score = 0

    details = {}


    # =====================
    # Moving Average
    # =====================

    close_price = price_history["Close"]

    ma20 = close_price.rolling(window=20).mean().iloc[-1]

    current_price = close_price.iloc[-1]


    if current_price > ma20:
        ma_score = 7
    else:
        ma_score = 3


    score += ma_score

    details["Moving Average"] = ma_score


    return {
        "technical_score": score,
        "details": details
    }



if __name__ == "__main__":

    print("Technical Analysis Module")
    print(calculate_technical_score(price_history))

    

