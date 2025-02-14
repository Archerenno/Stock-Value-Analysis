import yfinance as yf

divs_dict = {"2020":0, "2021":0, "2022":0, "2023":0, "2024":0}


def get_stock_data(ticker_symbol, treasury_10yr):
    no_div = False
    stock = yf.Ticker(ticker_symbol)
    
    try:
        for datetime, div in stock.dividends.items():
            for i in range(2024, 2019, -1):
                if str(datetime).startswith(str(i)):
                    divs_dict[str(i)] += div
        last_5yr_divs = list(divs_dict.values())
    except TypeError as e:
        print(e)
        no_div = True
    
    beta = stock.info.get('beta', None)
    cost_of_equity = treasury_10yr + beta * (treasury_10yr - 0.08)

    curr_price = stock.info.get("currentPrice", None)

    return last_5yr_divs, cost_of_equity, curr_price, no_div


def dividend_average_growth(last_5yr_divs):
    div_growths = []
    if last_5yr_divs[0] == 0:
        return None
    for i in range(1, len(last_5yr_divs[1:]) + 1):
        if last_5yr_divs[i] == 0:
            return None
        growth = (last_5yr_divs[i] - last_5yr_divs[i - 1]) / last_5yr_divs[i - 1]
        div_growths.append(growth)
    avg_div_growth = sum(div_growths)/len(div_growths)
    print(f"{(avg_div_growth * 100):.2f}%")
    return avg_div_growth



def calc_value(avg_div_growth, wacc):
    next_year_div = divs_dict["2024"] * (1 + avg_div_growth)
    value = next_year_div / (wacc - avg_div_growth)
    value_mos_adjusted = value * 0.7
    return value_mos_adjusted


def print_result(intrinsic_value, curr_price, ticker):
    print(f"Max buy price for {ticker} is ${intrinsic_value:.2f}")
    print(f"Current price of {ticker} is ${curr_price:.2f}")
    print("\n")
    if curr_price >= intrinsic_value:
        print(f"Therefore, {ticker} is Overvalued")
        return 0
    else:
        print(f"Therefore, {ticker} is Undervalued")
        return 1


def main(ticker, treasury_10yr):
    print("\nDividend Discount Model\n\n")
    last_5yr_divs, wacc, curr_price, no_div = get_stock_data(ticker)
    if no_div is True:
        return 0
    else:
        avg_div_growth = dividend_average_growth(last_5yr_divs)
        if avg_div_growth is not None:
            intrinsic_value = calc_value(avg_div_growth, wacc)
            return print_result(intrinsic_value, curr_price, ticker)
        else:
            print(f"{ticker} has issued no dividends in one of the last 5 years and therefore cannot be considered in this model")
            return 0