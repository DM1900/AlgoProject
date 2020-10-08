#!/usr/bin/python

#https://www.youtube.com/watch?v=DOHg16zcUCc

"""
#Dependencies:
#Start Python 
pip install pandas-datareader
pip install matplotlib
pip install pandas
pip install numpy
pip install datetime
"""

# imports:
print("Load imports")
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import matplotlib.pyplot as pyplt
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import csv

#
print("Load variables")
PriceHistory = 28 # no. of days data to gather
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
tickerlist = "tickerfile.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
tickers = ['AAPL']#,'AMZN','BP.L']
"""
def get_stats(stock_data):
    return {
        'last': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20),
        'long_rolling': stock_data.rolling(window=200)
    }
"""
def clean_data(stock_data,col):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')
"""
def create_plot(stock_data, ticker):
    stats = get_stats(stock_data)
    pyplt.subplots(figsize=(12,8))
    pyplt.plot(stock_data, label=ticker)
    pyplt.xlabel('Date')
    pyplt.ylabel('Adj Close (p)')
    pyplt.legend()
    pyplt.title('Stock ticker')
    pyplt.show()
"""
#df2 = pd.DataFrame()
df2 = pd.DataFrame(columns = ['Adj Close', 'Date', 'Ticker','RSI']) 
print(df2)

def get_data(ticker):
    print(ticker)
    print("gap")
    try:
        stock_data = data.DataReader(ticker,'yahoo',START_DATE,END_DATE)
        adj_close = clean_data(stock_data,'Adj Close')
        df = pd.DataFrame.from_dict(adj_close)
        #print(df)
        RSI_PERIOD = 14
        chg = df['Adj Close'].diff(1)
        gain = chg.mask(chg<0,0)
        loss = chg.mask(chg>0,0)
        #
        avg_gain = gain.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        #
        RS = abs(avg_gain / avg_loss)
        RSI = 100 - (100/(1+RS))
        RSI = RSI.tail(1)
        df['Date'] = END_DATE
        df['Ticker'] = ticker
        df['RSI'] = RSI
        df = (df[-1:])
        print("df is:")
        print(df)
        #df = pd.DataFrame({"a":[0],"b":[ticker],"c":[RSI]})
        print("df2 is:")
        df2.append(df, ignore_index=True)
        print(df2)
        
        #CSV_FILE = datetime.now().strftime('output/RSIData_%Y%m%d.csv')
        #df.to_csv(CSV_FILE,index=False)
        #to_clipboard(excel=True,sep=None)
        #print(NEW_DATA)
        #f = open("newfile.txt", "a")
        #f.write(NEW_DATA)
        #f.close

    except RemoteDataError:
        print('No data found for {t}'.format(t=ticker))

#print("get_data has been set, running it now")

for ticker in tickers:
    get_data(ticker)

#end