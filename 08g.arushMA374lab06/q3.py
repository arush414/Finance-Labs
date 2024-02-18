import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from pandas import to_datetime
import scipy.stats as stats

def plot_returns(df, stocks_name):
  interval = ['daily', 'weekly', 'monthly']
  df_initial = df.copy()
  plt.rcParams["figure.figsize"] = (20, 5)
  for sname in stocks_name:
    df = df_initial.copy()
    for intvl in interval:
      if intvl == 'weekly':
        df['Day'] = (to_datetime(df['Date'])).dt.day_name()
        df = df.loc[df['Day'] == 'Monday']
        del df['Day']
      elif intvl == 'monthly':
        df = df.groupby(pd.DatetimeIndex(df['Date']).to_period('M')).nth(0)
      x = np.log(df[sname]/df[sname].shift(1))
      mean = np.nanmean(np.array(x))
      std = np.nanstd(np.array(x))
      x = [(i - mean)/std for i in x]
      if intvl == 'daily':
        plt.subplot(1, 3, 1)
      elif intvl == 'weekly':
        plt.subplot(1, 3, 2)
      else:
        plt.subplot(1, 3, 3)
      n_bins = 40
      plt.hist(x, n_bins, density = True, edgecolor = 'black', linewidth = 0.4, color = 'yellow', label = 'Normalized returns')
      mu = 0
      variance = 1
      sigma = math.sqrt(variance)
      x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)  
      plt.plot(x, stats.norm.pdf(x, mu, sigma), color = 'green', label = 'density function, N(0, 1)')
      plt.xlabel('Returns')
      plt.ylabel('Normalised Frequency')
      plt.title('Normalized log returns with N(0, 1) for \n{} on {} basis'.format(sname, intvl))
      plt.legend()
      if intvl == 'monthly':
        plt.show()
    
df=pd.read_csv("bsedata1.csv")
cols=df.columns.to_list()
cols.pop(0)
plot_returns(df,cols)

df=pd.read_csv("nsedata1.csv")
cols=df.columns.to_list()
cols.pop(0)
plot_returns(df,cols)