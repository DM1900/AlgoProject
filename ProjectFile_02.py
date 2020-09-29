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
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import matplotlib.pyplot as pyplt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv
#
PastPrice = 28 # no. of days data to gather
START_DATE = str((datetime.today()- timedelta(days=PastPrice)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
tickerlist = "tickerfile.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
#tickers = ['AAPL']

def get_stats(stock_data):
    return {
        'last': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20),
        'long_rolling': stock_data.rolling(window=200)
    }

def clean_data(stock_data,col):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

def create_plot(stock_data, ticker):
    stats = get_stats(stock_data)
    pyplt.subplots(figsize=(12,8))
    pyplt.plot(stock_data, label=ticker)
    pyplt.xlabel('Date')
    pyplt.ylabel('Adj Close (p)')
    pyplt.legend()
    pyplt.title('Stock ticker')
    pyplt.show()

def get_data(ticker):
    try:
        stock_data = data.DataReader(ticker,'yahoo',START_DATE,END_DATE)
        adj_close = clean_data(stock_data,'Adj Close')
        df = pd.DataFrame.from_dict(adj_close)
        #print(df)
        RSI_PERIOD = 14
        chg = df['Adj Close'].diff(1)
        gain = chg.mask(chg<0,0)
        #df['gain'] = gain
        loss = chg.mask(chg>0,0)
        #df['loss'] = loss
        #
        avg_gain = gain.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        #
        RS = abs(avg_gain / avg_loss)
        RSI = 100 - (100/(1+RS))
        df['Ticker'] = ticker
        df['RSI'] = RSI
        df = (df[-1:])
        print(df[-1:])
        #print("Stock:",ticker,RSI[-1:])
        CSV_FILE = "output/csvfile.csv"
        df.to_csv(CSV_FILE,index=False)
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