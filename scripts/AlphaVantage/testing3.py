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
###
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
WAITTIME = 3

tickerlist = "tickers/AV/tickerfile_TRADELIST.txt"
tickerlist = "tickers/AV/tickerfile_TEST.txt"
tickerlist = "tickers/AV/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

def GetAPIkey(): # get a new API key each time the script runs
    #print("Get API Key")
    keys = "scripts/AlphaVantage/keys.txt"
    lines = open(keys).read().splitlines()
    global APIkey
    APIkey = random.choice(lines)

df = pd.DataFrame(columns=[])   # create empty dataframe
df2 = pd.DataFrame(columns=[])  # create empty dataframe

def get_data(ticker):
    TEMPdf = pd.DataFrame()   # create empty dataframe
    df = pd.DataFrame()   # create empty dataframe
    global df2
    print(ticker)
    GetAPIkey() # get a new API key each time the script runs
    ts = TimeSeries(key=APIkey, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=ticker)#;
    print(data)
    TEMPdf = df.append(data)
    print("Print TEMPdf")
    print(TEMPdf)
    TEMPdf = TEMPdf.drop(['02. open','03. high','04. low','06. volume','07. latest trading day'], axis=1)
    print("Print TEMPdf")
    print(TEMPdf)
    RS = 99
    #TEMPdf['RSI'] = RS
    #print(TEMPdf)
    df2 = df2.append(df)
    print("wait...")
    time.sleep(WAITTIME)

print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)

print(df2.tail(5))

#https://www.alphavantage.co/query?function=TimeSeries&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698