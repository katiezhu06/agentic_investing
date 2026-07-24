def get_watchlist():
    """
    Return the list of stocks to analyze.

    In the future, this function will retrieve the user's
    Robinhood watchlist through Robinhood MCP.
    """

    return [
        "AAPL",
        "MSFT",
        "NVDA",
        "META",
        "AMZN",
    ]


if __name__ == "__main__":
    print(get_watchlist())