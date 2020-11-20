#!/usr/bin/python
#https://www.youtube.com/watch?v=DOHg16zcUCc

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

###
print("Load variables")
PriceHistory = 180 # no. of days data to gather
RSI_PERIOD = 14 # no. of days to calculate RSI
###
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
tickerlist = "tickers/tickerfile.txt"
#tickerlist = "tickers/tickerfile_TEST.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
#tickers = ['AAPL','AMZN','BP.L','V','VHYL.L','BRKB','UKDV.L']
# create empty dataframe
df2 = pd.DataFrame(columns=[])#'Adj Close', 'Date', 'Ticker','RSI'

def clean_data(stock_data,col):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col].reindex(weekdays)
    return clean_data.fillna(method='ffill')

def get_data(ticker):
    try:
        print(ticker)
        global df
        global df2
        stock_data = data.DataReader(ticker,'yahoo',START_DATE,END_DATE)
        adj_close = clean_data(stock_data,'Adj Close')
        df = pd.DataFrame.from_dict(adj_close)
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
        #df['Date'] = END_DATE
        df['Ticker'] = ticker
        df['RSI'] = RSI
        df = (df[-1:])
        df2 = df2.append(df)
        print("success on " + ticker)# + ", RSI is " + RSI)
    except RemoteDataError:
        print('No data found for {t}'.format(t=ticker))

print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)

df2 = df2.sort_values(by=['RSI'], na_position='last')

print(df2)

CSV_FILE = datetime.now().strftime('output/RSIData_%Y%m%d.csv')
df2.to_csv(CSV_FILE,index=False)
#end