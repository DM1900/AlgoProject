#!/usr/bin/python
#https://www.youtube.com/watch?v=DOHg16zcUCc

# imports:
print("Load imports")
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
#import matplotlib as plt
#import matplotlib.pyplot as pyplt
import pandas as pd
#import numpy as np
from datetime import datetime, timedelta
import csv

###
#print(datetime.now())
print("Load variables")
PriceHistory = 180 # no. of days data to gather
RSI_PERIOD = 14 # no. of days to calculate RSI
RSILOW = 45
RSIHIGH = 65
HOLD = "-"
###
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
tickerlist = "tickers/tickerfile.txt"
tickerlist = "tickers/tickerfile_TRADELIST.txt"
#tickerlist = "tickers/tickerfile_TEST.txt"
#tickerlist = "tickers/tickerfile_TEST_UK.txt"
#tickerlist = "tickers/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
    
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
        adj_close = round(clean_data(stock_data,'Adj Close'),2)
        df = pd.DataFrame.from_dict(adj_close)
        OPEN = round(stock_data.Open.tail(1),2)
        df['Open'] = OPEN
        #CLOSE = stock_data.Close.tail(1)
        #df['Close'] = CLOSE
        chg = df['Adj Close'].diff(1)
        #
        gain = chg.mask(chg<0,0)
        loss = chg.mask(chg>0,0)
        avg_gain = gain.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        avg_loss = loss.ewm(com=RSI_PERIOD-1,min_periods=RSI_PERIOD).mean()
        RS = abs(avg_gain / avg_loss)
        RSI = 100 - (100/(1+RS))
        RSI = round(RSI.tail(1),2)
        #df['Date'] = END_DATE
        OPEN = df[-1:].iat[0,1]
        CLOSE = df[-1:].iat[0,0]
        CHANGE = round(((CLOSE/OPEN)-1)*100,2)
        CHANGE = str(CHANGE) + "%"
        df['Change'] = CHANGE
        df['RSI'] = RSI
        df['Ticker'] = ticker
        RSI = df[-1:].iat[0,3]
        if RSI > RSIHIGH:
            if CLOSE < OPEN:
                print("BUY")
                df['Suggestion'] = "SELL"
            else:
                df['Suggestion'] = HOLD
        elif RSI < RSILOW:
            if CLOSE > OPEN:
                print("BUY")
                df['Suggestion'] = "BUY"
            else:
                df['Suggestion'] = HOLD
        else:
            df['Suggestion'] = HOLD
        df = (df[-1:])
        df2 = df2.append(df)
        #print("success on " + ticker)# + ", RSI is " + RSI)
    except RemoteDataError:
        print('No data found for {t}'.format(t=ticker))

print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)

#df2 = df2.sort_values(by=['Suggestion'], na_position='last')

print(df2.tail(5))

CSV_FILE = datetime.now().strftime('output/RSIData_Extended_%Y%m%d.csv')
df2.to_csv(CSV_FILE,index=False)

#print(datetime.now())

#end