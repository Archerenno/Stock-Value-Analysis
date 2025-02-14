import yfinance as yf

def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    # Get dividend yield
    dividend_yield = stock.info.get("dividendYield", None) # Returns None if the specified metric is not found in the dict
    if dividend_yield is not None:
        dividend_yield *= 100

    # Get expected 1-year growth from analysis
    growth_estimates = stock.get_growth_estimates(as_dict=True)
    expected_1y_growth = growth_estimates['stockTrend']['+1y']

    # Get P/E Ratio (Earnings Per Share)
    try:
        trailing_PE = stock.get_info()['trailingPE']
        return dividend_yield, expected_1y_growth * 100, trailing_PE
    except KeyError as k:
        return dividend_yield, expected_1y_growth * 100, None

    


def peter_lynch_val(exp_growth, div_yield, PE_ratio, stock):
    result = (exp_growth + div_yield) / PE_ratio
    print(f"Result Value was: {result:.2f}")
    print("\n")
    if result < 1:
        print(f"According to Peter Lynch Method, {stock} is Overvalued")
        return 0
    elif result >= 1 and result < 1.5:
        print(f"According to Peter Lynch Method, {stock} is Fairly Valued")
        return 0
    elif result >= 1.5 and result < 2:
        print(f"According to Peter Lynch Method, {stock} is Under Valued")
        return 1
    else:
        print(f"According to Peter Lynch Method, {stock} is Very Under Valued")
        return 1
    

def main(ticker):
    print("\nPeter Lynch Method\n\n")
    div_yield, exp_growth_1y, ttm_pe = get_stock_data(ticker)
    if div_yield is None:
        print(f"{ticker} has issued no dividends and therefore cannot be considered by the Peter Lynch Model")
        return 0
    elif ttm_pe is None:
        print(f"{ticker} does not have a PE and therefore cannot be considered by the Peter Lynch Model (profit is less than or equal to $0 ttm)")
        return 0
    else:
        return peter_lynch_val(exp_growth_1y, div_yield, ttm_pe, ticker)

