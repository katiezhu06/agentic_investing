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

    "return_on_equity": info.get("returnOnEquity"),
    "profit_margins": info.get("profitMargins"),

    }
    
def get_price_history(symbol):

    stock = yf.Ticker(symbol)

    history = stock.history(period="6mo")

    if history.empty:
        return None

    history = history.dropna(subset=["Close"])

    return history



if __name__ == "__main__":

    data = get_stock_info("AAPL")

    print(data)

    history = get_price_history("AAPL")

    print(history.head())
    
 