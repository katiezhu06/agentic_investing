from data.watchlist import get_watchlist
from data.market_data import get_stock_info
from analysis.fundamental_analysis import calculate_fundamental_score


watchlist = get_watchlist()


for stock in watchlist:

    stock_info = get_stock_info(stock)

    result = calculate_fundamental_score(stock_info)

    print(stock)
    print(result)
    print("--------------------------------")
