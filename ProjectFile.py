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
#print("Finished Imports")
#print("Define Variables")
#START_DATE = '2020-01-01'
PastPrice = 28
START_DATE = str((datetime.today()- timedelta(days=PastPrice)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
#print(START_DATE, END_DATE)
#UK_STOCK = 'BP'
#USA_STOCK = 'AMZN'
USA_STOCK = 'BP'
tickers = ['AAPL','BP']
#print(UK_STOCK, USA_STOCK)
#print(tickers)
period = -14

def get_stats(stock_data):
    #print("***get_stats***")
    return {
        'last': np.mean(stock_data.tail(1)),
        'short_mean': np.mean(stock_data.tail(20)),
        'long_mean': np.mean(stock_data.tail(200)),
        'short_rolling': stock_data.rolling(window=20),
        'long_rolling': stock_data.rolling(window=200)
    }

def clean_data(stock_data,col):
    #print("***clean_data***")
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

def create_plot(stock_data, ticker):
    #print("***create_plot***")
    stats = get_stats(stock_data)
    pyplt.subplots(figsize=(12,8))
    pyplt.plot(stock_data, label=ticker)
    pyplt.xlabel('Date')
    pyplt.ylabel('Adj Close (p)')
    pyplt.legend()
    pyplt.title('Stock ticker')
    pyplt.show()

def get_data(ticker):
    #print("***get_data***")
    try:
        stock_data = data.DataReader(ticker,'yahoo',START_DATE,END_DATE)
        adj_close = clean_data(stock_data,'Adj Close')
        #print(adj_close)
        #create_plot(adj_close, ticker)
        #print(stock_data)
        # RSI = 100 - (100 /(1+RS))
        #recent = adj_close[period:]
        df = pd.DataFrame.from_dict(adj_close)
        RSI_PERIOD = 14
        chg = df['Adj Close'].diff(1)
        #print(chg)
        
        gain = chg.mask(chg<0,0)
        df['gain'] = gain
        loss = chg.mask(chg>0,0)
        df['loss'] = loss

        avg_gain = gain.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()

        RS = abs(avg_gain / avg_loss)

        RSI = 100 - (100/(1+RS))

        #df['RSI'] = RSI

        #print(df)
        #print(df[-1:])
        print("Stock:",ticker,RSI[-1:])
        #print(RSI[-1:])


    except RemoteDataError:
        print('No data found for {t}'.format(t=ticker))

#print("get_data has been set, running it now")

#get_data(USA_STOCK)

for ticker in tickers:
    get_data(ticker)

#end