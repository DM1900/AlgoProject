#!/usr/bin/python
# imports:
print("Load imports")
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.techindicators import 
import sys
import random
import time
from datetime import datetime, timedelta
import csv

#variables
print(datetime.now())
print("Load variables")
PriceHistory = 180 # no. of days data to gather
RSI_PERIOD = 14 # no. of days to calculate RSI
RSILOW = 45
RSIHIGH = 65
HOLD = "-"
###
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
WAITTIME = 3

tickerlist = "tickers/AV/tickerfile_TRADELIST.txt"
tickerlist = "tickers/AV/tickerfile_TEST.txt"
#tickerlist = "tickers/AV/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

def GetAPIkey(): # get a new API key each time the script runs
    #print("Get API Key")
    keys = "scripts/AlphaVantage/keys.txt"
    lines = open(keys).read().splitlines()
    global APIkey
    APIkey = random.choice(lines)

#df = pd.DataFrame(columns=[])   # create empty dataframe
df2 = pd.DataFrame(columns=[])  # create empty dataframe

def get_data(ticker):
    TEMPdf = pd.DataFrame()   # create empty dataframe
    df = pd.DataFrame()   # create empty dataframe
    global df2
    print(ticker)
    GetAPIkey() # get a new API key each time the script runs
    ts = TimeSeries(key=APIkey, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=ticker)#;
    #print("PRINT data")
    #print(data)
    TEMPdf = df.append(data)
    #print("Print TEMPdf")
    #print(TEMPdf)
    DTICKER = TEMPdf.iat[0,0]
    df = df.append({'Ticker':DTICKER}, ignore_index=True)
    #df['Ticker'] = DTICKER
    DPRICE = TEMPdf.iat[0,4]
    df['Price'] = DPRICE
    DCLOSE = TEMPdf.iat[0,7]
    df['PreviousClose'] = DCLOSE
    RS = 99 # this needs to be scripted correctly
    df['RSI'] = RS
    if RS > RSIHIGH:
        if DCLOSE < DPRICE:
            #print("BUY")
            df['Suggestion'] = "SELL"
        else:
            df['Suggestion'] = HOLD
    elif RS < RSILOW:
        if CLOSE > DPRICE:
            #print("BUY")
            df['Suggestion'] = "BUY"
        else:
            df['Suggestion'] = HOLD
    else:
        df['Suggestion'] = HOLD
    #print("Print 'df'")
    #print(df)
    df2 = df2.append(df)
    #print("wait...")
    time.sleep(WAITTIME)

print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)

print("PRINT df2")
print(df2)
#print(df2.tail(5))

#https://www.alphavantage.co/query?function=TimeSeries&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698
