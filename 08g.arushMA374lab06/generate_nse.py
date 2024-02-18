import yfinance as yf
import pandas as pd
market_nse=['^NSEI']
nse= ['ACC.NS', 'GODREJIND.NS', 'HINDZINC.NS', 'IDEA.NS', 'IGL.NS',
          'LUPIN.NS', 'MAHABANK.NS', 'MGL.NS', 'PAGEIND.NS', 'TATACHEM.NS']
non_nse=['HAVELLS.NS', 'HAL.NS', 'ICICIGI.NS', 'ICICIPRULI.NS', 'AMBUJACEM.NS', 
           'IOC.NS', 'NAUKRI.NS', 'INDIGO.NS', 'JINDALSTEL.NS', 'BANKBARODA.NS']
stocks=market_nse+nse+non_nse

start_date = '2019-01-01'
end_date = '2023-12-31'
data = yf.download(stocks, start=start_date, end=end_date)
closing_prices = data['Close']
closing_prices=closing_prices[ stocks]
closing_prices.rename(columns={market_nse[0]: "NIFTY50"}, inplace=True)
closing_prices.to_csv('nsedata1.csv')
