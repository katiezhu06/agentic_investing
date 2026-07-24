from data.watchlist import get_watchlist
from data.market_data import get_stock_info, get_price_history
from analysis.fundamental_analysis import calculate_fundamental_score
from analysis.technical_analysis import calculate_technical_score


watchlist = get_watchlist()


for stock in watchlist:

    print("--------------------------------")
    print("Checking:", stock)

    stock_info = get_stock_info(stock)

    price_history = get_price_history(stock)

    if price_history is None:
        print("No price data")
        continue

    fundamental_score = calculate_fundamental_score(stock_info)

    technical_score = calculate_technical_score(price_history)


    print("Fundamental:")
    print(fundamental_score)

    print("Technical:")
    print(technical_score)