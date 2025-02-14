import yfinance as yf

def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    # Get dividend yield
    ttm_eps = stock.info.get("trailingEps", None)

    growth_estimates = stock.get_growth_estimates(as_dict=True)
    expected_1y_growth = growth_estimates['stockTrend']['+1y']
    
    trailing_PE = stock.info.get('trailingPE', None)

    curr_price = stock.info.get("currentPrice", None)

    return ttm_eps, expected_1y_growth, trailing_PE, curr_price


def investing_ph_val(ttm_eps, expected_1y_growth, trailing_PE, curr_price, ticker):
    fiv = ttm_eps * ((1 + expected_1y_growth)**5)*trailing_PE
    piv = fiv / (1.15 ** 5)
    max_buy_mos_adjusted = piv * 0.7
    print(f"The max buy price for {ticker} is {max_buy_mos_adjusted}")
    print(f"The current price for {ticker} is {curr_price}")
    print("\n")
    if max_buy_mos_adjusted <= curr_price:
        print(f"Therefore {ticker} is Overpriced")
        return 0
    else:
        print(f"Therefore {ticker} is Undervalued")
        return 1

    

def main(ticker):
    print("\nInvesting PH Method\n\n")
    ttm_eps, expected_1y_growth, trailing_PE, curr_price = get_stock_data(ticker)
    return investing_ph_val(ttm_eps, expected_1y_growth, trailing_PE, curr_price, ticker)

