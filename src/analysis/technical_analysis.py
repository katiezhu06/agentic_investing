def calculate_rsi(history):

    close = history["Close"]

    delta = close.diff()

    gain = delta.clip(lower=0)

    loss = -delta.clip(upper=0)


    average_gain = gain.rolling(window=14).mean()

    average_loss = loss.rolling(window=14).mean()


    rs = average_gain / average_loss

    rsi = 100 - (100 / (1 + rs))


    return rsi

def calculate_rsi_score(rsi):

    if rsi < 30:
        return 8

    elif rsi < 50:
        return 6

    elif rsi < 70:
        return 7

    else:
        return 3

def calculate_volume_ratio(history):

    volume = history["Volume"]

    average_volume = volume.rolling(window=20).mean().iloc[-1]

    current_volume = volume.iloc[-1]

    volume_ratio = current_volume / average_volume

    return volume_ratio


def calculate_volume_ratio_score(volume_ratio):

    if volume_ratio > 1.5:
        return 5

    elif volume_ratio > 1:
        return 3

    else:
        return 1

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

    # =====================
    # RSI
    # =====================
    rsi = calculate_rsi(price_history)

    latest_rsi = rsi.iloc[-1]

    rsi_score = calculate_rsi_score(latest_rsi)

    score += rsi_score

    details["RSI"] = rsi_score

    # =====================
    # Volume Ratio
    # =====================
    volume_ratio = calculate_volume_ratio(price_history)

    volume_ratio_score = calculate_volume_ratio_score(volume_ratio)

    score += volume_ratio_score

    details["Volume Ratio"] = volume_ratio_score

    # =====================
    # Technical Score
    # =====================

    return {
    "technical_score": score,
    "details": details,
}

    


