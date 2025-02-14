import benjamin_graham as bg
import discounted_cashflow as dc
import peter_lynch as pl
import investing_PH as ip
import dividend_discount as dd
import investing_w_tom as iwt
import yfinance as yf
import json
import csv

with open("us_company_tickers.json", "r") as file:  # Replace with your actual filename
    data = json.load(file)
    us_tickers = []
    for ticker_num, ticker_dict in data.items():
        us_tickers.append(ticker_dict['ticker'])


def run_analysis_one_stock():
    print("\n")
    ticker = input("Enter stock ticker: ")
    print("\n------------------------------------------------------\n")
    stock = yf.Ticker(ticker)
    print(f"Company Name: {stock.info.get('shortName', 'Unknown')}")
    print("\n------------------------------------------------------\n")

    value_score = 0
    treasury_10yr = float(input("Enter the 10yr Treasury Yield of the country you are searching in (Decimal Form): "))

    value_score = bg.main(ticker)
    print("\n------------------------------------------------------\n")
    value_score += dc.main(ticker)
    print("\n------------------------------------------------------\n")
    value_score += pl.main(ticker)
    print("\n------------------------------------------------------\n")
    value_score += ip.main(ticker)
    print("\n------------------------------------------------------\n")
    value_score += dd.main(ticker, treasury_10yr)
    print("\n------------------------------------------------------\n")
    value_score += iwt.main(ticker)
    print("\n------------------------------------------------------\n")
    print(f"Stock score is {value_score}/6")
    print("\n------------------------------------------------------")


def evaluate_market():
    for ticker in us_tickers:
        run_analysis_one_stock(ticker)


evaluate_market()
# run_analysis_one_stock()