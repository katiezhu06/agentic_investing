from src.data.watchlist import get_watchlist
from src.analysis.investment_score import calculate_investment_score


watchlist = get_watchlist()


for stock in watchlist:

    print("--------------------------------")
    print("Checking:", stock)


    result = calculate_investment_score(stock)


    print(result)