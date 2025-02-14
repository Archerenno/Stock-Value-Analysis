import yfinance as yf
import math

millnames = ['',' Thousand',' Million',' Billion',' Trillion']


def get_stock_data(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    
    cashflow_dict = stock.get_cashflow(as_dict=True, pretty=True)
    free_cash_flow = list(cashflow_dict.items())[0][1]['Free Cash Flow']
    market_cap = stock.info.get('marketCap', None)

    cash_assets = stock.info.get('totalCash', None)

    return free_cash_flow, market_cap, cash_assets


def growth_10percent(fcf, price_to_fcf):
    fcf_list = [fcf]
    for i in range(2026, 2036):
        fcf *= 1.1
        fcf_list.append(fcf)
    fcf_final = fcf_list[-1]
    i = 0
    discounted_15percent_list = [-1]
    for fcf in fcf_list:
        if i != 0:
            discounted = fcf / (1.15 ** i)
            discounted_15percent_list.append(discounted)
        i += 1
    terminal_value = fcf_final * price_to_fcf
    discounted_term_value = terminal_value / (1.15 ** 10)
    discounted_15percent_list.append(discounted_term_value)
    intrinsic_value = sum(discounted_15percent_list[1:])
    return intrinsic_value
    

def growth_15percent(fcf, price_to_fcf):
    fcf_list = [fcf]
    for i in range(2026, 2036):
        fcf *= 1.15
        fcf_list.append(fcf)
    fcf_final = fcf_list[-1]
    i = 0
    discounted_15percent_list = [-1]
    for fcf in fcf_list:
        if i != 0:
            discounted = fcf / (1.15 ** i)
            discounted_15percent_list.append(discounted)
        i += 1
    terminal_value = fcf_final * price_to_fcf
    discounted_term_value = terminal_value / (1.15 ** 10)
    discounted_15percent_list.append(discounted_term_value)
    intrinsic_value = sum(discounted_15percent_list[1:])
    return intrinsic_value


def value_range(intrinsic_val_10cent, intrinsic_val_15cent, cash_assets):
    lower_value_inc_cash = intrinsic_val_10cent + cash_assets
    upper_value_inc_cash = intrinsic_val_15cent + cash_assets
    lower_value_mos = lower_value_inc_cash * 0.7
    upper_value_mos = upper_value_inc_cash * 0.7
    return lower_value_mos, upper_value_mos


def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1,
                        int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))

    return '{:.2f}{}'.format(n / 10**(3 * millidx), millnames[millidx])



def print_result(lower_value, upper_value, market_cap, ticker):
    print(f"The lower value of {ticker} is {millify(lower_value)}")
    print(f"The upper value of {ticker} is {millify(upper_value)}")
    print(f"The current value of {ticker} is {millify(market_cap)}")
    print("\n")
    if market_cap >= upper_value:
        print(f"Therfore, {ticker} is Fairly Valued/OverValued")
        return 0
    elif market_cap <= lower_value:
        print(f"Therfore, {ticker} is Very UnderValued")
        return 1
    else:
        print(f"Therfore, {ticker} is Undervalued")
        return 1



def main(ticker):
    print("\nDiscounted Cashflow (Warren Buffet) Method\n\n")
    free_cash_flow, market_cap, cash_assets = get_stock_data(ticker)
    price_to_fcf = market_cap/free_cash_flow
    intrinsic_val_10cent = growth_10percent(free_cash_flow, price_to_fcf)
    intrinsic_val_15cent = growth_15percent(free_cash_flow, price_to_fcf)
    lower_value, upper_value = value_range(intrinsic_val_10cent, intrinsic_val_15cent, cash_assets)
    return print_result(lower_value, upper_value, market_cap, ticker)