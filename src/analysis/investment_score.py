from src.analysis.fundamental_analysis import calculate_fundamental_score
from src.data.market_data import get_stock_info
from src.analysis.technical_analysis import calculate_technical_score
from src.analysis.market_analysis import calculate_market_score

from src.data.market_data import get_price_history


def calculate_investment_score(symbol):

    stock_data = get_stock_info(symbol)

    fundamental = calculate_fundamental_score(stock_data)

    history = get_price_history(symbol)

    technical = calculate_technical_score(history)

    market = calculate_market_score()


    total_score = (
        fundamental["fundamental_score"]
        +
        technical["technical_score"]
        +
        market["market_score"]
    )


    return {
        "symbol": symbol,
        "fundamental": fundamental,
        "technical": technical,
        "market": market,
        "total_score": total_score
    }



if __name__ == "__main__":

    result = calculate_investment_score("AAPL")

    print(result)