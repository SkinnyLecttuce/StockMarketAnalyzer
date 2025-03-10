import yfinance as yf
import pandas as pd

#a CSV that has all your tickers
ticker_df = pd.read_csv("stocks//tickers.csv") 
all_tickers = ticker_df["Ticker"].tolist()  #or adjust column name as needed

#download data for each ticker 
for ticker in all_tickers:
    print(f"Downloading data for {ticker}...")
    data = yf.download(ticker, period="max")
    if not data.empty:
        data.to_csv(f"{ticker}.csv")
    else:
        print(f"No data found for {ticker} (possibly delisted or invalid).")
