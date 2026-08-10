def calculate_fundamental_score(stock_data):

    score = 0

    details = {}

    # =====================
    # 1. ROE Score (7 pts)
    # =====================

    roe = stock_data.get("return_on_equity")

    if roe is not None:

        if roe > 0.25:
            roe_score = 8

        elif roe > 0.15:
            roe_score = 6

        elif roe > 0.10:
            roe_score = 3

        else:
            roe_score = 1

    else:
        roe_score = 0


    score += roe_score
    details["ROE"] = roe_score


    # =====================
    # 2. Profit Margin Score (8 pts)
    # =====================

    margin = stock_data.get("profit_margins")


    if margin is not None:

        if margin > 0.25:
            margin_score = 8

        elif margin > 0.15:
            margin_score = 6

        elif margin > 0.05:
            margin_score = 4

        else:
            margin_score = 1

    else:
        margin_score = 0


    score += margin_score
    details["Profit Margin"] = margin_score



    # =====================
    # 3. P/E Ratio Score (10 pts)
    # =====================

    pe = stock_data.get("pe_ratio")


    if pe is not None:

        if 10 <= pe <= 25:
            pe_score = 7

        elif 25 < pe <= 35:
            pe_score = 5

        elif 35 < pe <= 50:
            pe_score = 3

        else:
            pe_score = 1

    else:
        pe_score = 0


    score += pe_score
    details["PE Ratio"] = pe_score



    # =====================
    # 4. EPS Score (10 pts)
    # =====================

    eps = stock_data.get("eps")


    if eps is not None:

        if eps > 10:
            eps_score = 7

        elif eps > 5:
            eps_score = 7

        elif eps > 0:
            eps_score = 5

        else:
            eps_score = 3

    else:
        eps_score = 0


    score += eps_score
    details["EPS"] = eps_score



    return {
        "fundamental_score": score,
        "details": details
    }



if __name__ == "__main__":

    apple = {
        "return_on_equity": 1.41,
        "profit_margins": 0.27,
        "pe_ratio": 38.4,
        "eps": 8.19
    }


    result = calculate_fundamental_score(apple)

    print(result)