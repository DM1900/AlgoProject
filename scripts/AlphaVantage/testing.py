#!/usr/bin/python
# imports:
print("Load imports")
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators 
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
    #print(APIkey)

df2 = pd.DataFrame(columns=[])  # create empty dataframe

def get_data(ticker):
    GetAPIkey()
    TEMPdf = pd.DataFrame()   # create empty dataframe
    ti = TechIndicators(key=APIkey, output_format='pandas')
    dataRSI = ti.get_rsi(symbol=ticker,interval='daily', time_period=14)
    dataRSI = dataRSI[0]
    TEMPdf = TEMPdf.append(dataRSI)
    TEMPdf = TEMPdf.iloc[-1]
    print(TEMPdf)


print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)

