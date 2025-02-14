import yfinance as yf

PE_NO_GROWTH = 7
AVG_AA_BOND_YIELD_PERCENT = 4.4


def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    # move these two lines of code to a more suitable place because this place assumes their order of function call

    ttm_eps = stock.info.get("trailingEps", None)

    # This needs to be changed manually every month
    curr_AAA_bond_yield = 5.46

    growth_estimates = stock.get_growth_estimates(as_dict=True)
    expected_1y_growth = growth_estimates['stockTrend']['+1y']

    curr_price = stock.info.get("currentPrice", None)

    return ttm_eps, curr_AAA_bond_yield, expected_1y_growth, curr_price


def benj_graham(ttm_eps, curr_AAA_bond_yield, expected_1y_growth, curr_price, ticker):

    value = (ttm_eps * (8.5 + (2 * expected_1y_growth)) * 4.4)/curr_AAA_bond_yield
    value_mos_adjusted = value * 0.7
    print(f"The max buy price for {ticker} is {value}")
    print(f"The current value of {ticker} is {curr_price}")
    print("\n")
    if value_mos_adjusted <= curr_price:
        print(f"Therefore {ticker} is Overpriced")
        return 0
    else:
        print(f"Therefore {ticker} is Undervalued")
        return 1

    

def main(ticker):
    print("\nBenjamin Graham Method\n\n")
    ttm_eps, curr_AAA_bond_yield, expected_1y_growth, curr_price = get_stock_data(ticker)
    return benj_graham(ttm_eps, curr_AAA_bond_yield, expected_1y_growth, curr_price, ticker)

