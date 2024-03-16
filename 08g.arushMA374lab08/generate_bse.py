import yfinance as yf
import pandas as pd
market_bse=['^BSESN']

bse = ['WIPRO.BO', 'BAJAJ-AUTO.BO', 'HDFCBANK.BO', 'HEROMOTOCO.BO', 'TCS.BO',
          'INFY.BO', 'BAJFINANCE.BO', 'MARUTI.BO', 'RELIANCE.BO', 'TATAMOTORS.BO']
nonbse=['ZOMATO.BO','ZEEL.BO','TVSMOTOR.BO','PIDILITIND.BO','NAUKRI.BO','IRCTC.BO','DLF.BO','COLPAL.BO','MFSL.BO','BANKBARODA.BO']

stocks=market_bse+bse+nonbse
start_date = '2019-01-01'
end_date = '2023-12-31'
data = yf.download(stocks, start=start_date, end=end_date)
closing_prices = data['Close']
closing_prices=closing_prices[ stocks]
closing_prices.rename(columns={market_bse[0]: "Sensex"}, inplace=True)
closing_prices.to_csv('bsedata1.csv')   