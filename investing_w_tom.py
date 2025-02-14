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


def calc_intrinsic_val(ttm_eps, expected_1y_growth, trailing_PE):
    eps_by_year = [ttm_eps]
    for i in range(1, 10):
        ttm_eps = ttm_eps + (ttm_eps * expected_1y_growth)
        eps_by_year.append(ttm_eps)
    eps_10yrs = eps_by_year[-1]
    share_value_10yrs = eps_10yrs * trailing_PE
    for i in range(1, 10):
        share_value_10yrs *= 0.85
    intrinsic_val = share_value_10yrs
    intrinsic_val_mos = intrinsic_val * 0.7
    return intrinsic_val_mos


def print_result(intrinsic_val, curr_price, ticker):
    print(f"The intrinsic value of {ticker} is {intrinsic_val:.2f}")
    print(f"The current price of {ticker} is {curr_price:.2f}")
    print("\n")
    if intrinsic_val >= curr_price:
        print(f"Therefore, {ticker} is Undervalued")
        return 1
    else:
        print(f"Therefore, {ticker} is Overvalued")
        return 0



def main(ticker):
    print("\nInvesting w Tom Method\n\n")
    ttm_eps, expected_1y_growth, ttm_PE, curr_price = get_stock_data(ticker)
    value = calc_intrinsic_val(ttm_eps, expected_1y_growth, ttm_PE)
    return print_result(value, curr_price, ticker)