import yfinance as yf
import pandas as pd

def download_stock_data():
    indian_stock_tickers = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "WIPRO.NS",
        "MARUTI.NS",
        "AXISBANK.NS",
        "HINDUNILVR.NS",
        "TITAN.NS",
        "HEROMOTOCO.NS",
        "BHARTIARTL.NS"
    ]

    data = yf.download(indian_stock_tickers, end="2024-02-01", start="2019-02-01",interval="1mo")['Adj Close']
    data=data.tail(60)
    data.to_csv('210123008.csv')
    
    
download_stock_data()