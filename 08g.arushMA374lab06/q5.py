import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from pandas import to_datetime

def plot_stock_prices(df1, df2, sname, intvl):
  x = df1['Date'].to_list()
  y1 = df1[sname].to_list()
  y2 = df2[sname].to_list()
  plt.rcParams["figure.figsize"] = (20, 5)
  if intvl == 'weekly':
    plt.subplot(1, 2, 1)
  else:
    plt.subplot(1, 2, 2)
  plt.plot(x, y2, color = 'green', label = 'Predicted Price')
  plt.plot(x, y1, color = 'blue', label = 'Original Price')
  plt.xticks(np.arange(0, len(x), int(len(x)/4)), df1['Date'][0:len(x):int(len(x)/4)])
  plt.title('Plot for Stock prices for {} on {} basis'.format(sname, intvl))
  plt.xlabel('Time')
  plt.ylabel('Price')
  plt.grid(True)
  plt.legend()
  if intvl == 'monthly':
    plt.show()  

def generate_path(df, stocks_name):
  df = df.fillna(method ='bfill')
  interval = ['weekly', 'monthly']
  initial_df = df.copy()  
  for sname in stocks_name:
    df = initial_df.copy()
    for intvl in interval:
      delta_t = 1/252
      df = initial_df.copy()
      if intvl == 'weekly':
        df['Day'] = (to_datetime(df['Date'])).dt.day_name()
        df = df.loc[df['Day'] == 'Monday']
        del df['Day']
        delta_t = 7/252
      elif intvl == 'monthly':
        df = df.groupby(pd.DatetimeIndex(df['Date']).to_period('M')).nth(0)
        delta_t = 30/252
      df_original = df.copy()
      df_training = df.loc[ (to_datetime(df['Date'])).dt.year <= 2022]
      df_predicted = df.loc[ (to_datetime(df['Date'])).dt.year > 2022]
      df_predicted.set_index('Date', inplace = True)
      x = np.log(df_predicted[sname]/df_predicted[sname].shift(1))    
      mean = np.nanmean(np.array(x)) 
      var = np.nanvar(np.array(x))
      factor = 0
      if intvl == 'weekly':
        factor = 52
      else:
        factor = 12      
      mean *= factor
      var *= (len(x) * factor) / (len(x) - 1)
      mean += 0.5 * var
      np.random.seed(20)      
      S0 = df_training.iloc[len(df_training) - 1][sname]
      for idx, row in df_predicted.iterrows():
        S = S0 * math.exp((mean - 0.5 * var) * delta_t + math.sqrt(var) * math.sqrt(delta_t) * np.random.normal(0, 1))
        S0 = S
        row[sname] = S
      df_predicted = df_training.append(df_predicted, ignore_index=True)
      plot_stock_prices(df_original, df_predicted, sname, intvl)

df=pd.read_csv("bsedata1.csv")
cols=df.columns.to_list()
cols.pop(0)
generate_path(df,cols)

df=pd.read_csv("nsedata1.csv")
cols=df.columns.to_list()
cols.pop(0)
generate_path(df,cols)