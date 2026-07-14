import yfinance as yf


def get_stock_info(symbol):
    stock = yf.Ticker(symbol)

    info = stock.info

    return {
    "company": info.get("longName"),
    "sector": info.get("sector"),

    "current_price": info.get("currentPrice"),
    "market_cap": info.get("marketCap"),

    "pe_ratio": info.get("trailingPE"),
    "eps": info.get("trailingEps"),

    "volume": info.get("volume"),
    "average_volume": info.get("averageVolume"),

    "52_week_high": info.get("fiftyTwoWeekHigh"),
    "52_week_low": info.get("fiftyTwoWeekLow"),
}


if __name__ == "__main__":
    data = get_stock_info("AAPL")

    print(data)