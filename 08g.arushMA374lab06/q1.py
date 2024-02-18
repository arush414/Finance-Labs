import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import to_datetime
      
def plot(df):
  df1=df.copy()
  df1['Day'] = (to_datetime(df1['Date'])).dt.day_name()
  df1 = df1.loc[df1['Day'] == 'Monday']
  del df1['Day']
  df2 = df.copy()
  df2 = df2.groupby(pd.DatetimeIndex(df2['Date']).to_period('M')).nth(0)

  for i in range(21):
    plt.rcParams["figure.figsize"] = (20, 5)
    plt.subplot(1,3,1)
    x=df[df.columns[0]].to_list()
    plt.plot(x,df[df.columns[i+1]])
    plt.xticks(np.arange(0, len(x), int(len(x)/3)), df['Date'][0:len(x):int(len(x)/3)])
    plt.xlabel('Time')
    plt.ylabel('Price')
    s="Daily stock price vs time plot for "+ df.columns[i+1]
    plt.title(s)
    plt.grid(True)
    plt.subplot(1,3,2)
    x1=df1[df1.columns[0]].to_list()
    plt.plot(x1,df1[df1.columns[i+1]])
    plt.xticks(np.arange(0, len(x1), int(len(x1)/3)), df1['Date'][0:len(x1):int(len(x1)/3)])
    plt.xlabel('Time')
    plt.ylabel('Price')
    s="Weekly stock price vs time plot for "+ df1.columns[i+1]
    plt.title(s)
    plt.grid(True)
    plt.subplot(1,3,3)
    x2=df2[df2.columns[0]].to_list()
    plt.plot(x2,df2[df2.columns[i+1]])
    plt.xticks(np.arange(0, len(x2), int(len(x2)/3)), df2['Date'][0:len(x2):int(len(x2)/3)])
    plt.xlabel('Time')
    plt.ylabel('Price')
    s="Monthly stock price vs time plot for "+ df2.columns[i+1]
    plt.title(s)
    plt.grid(True)
    plt.show()
  
df=pd.read_csv("bsedata1.csv")
plot(df)
df=pd.read_csv("nsedata1.csv")
plot(df)