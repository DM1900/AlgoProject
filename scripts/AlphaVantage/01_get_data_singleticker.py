#!/usr/bin/python3.9
# imports:
print("Load imports")
import pandas as pd
from pandas_datareader import data
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators 
import sys
import random

RSI_PERIOD = 14 # no. of days to calculate RSI
RSI_INT = 'daily' # interval to calculate RSI

tickers = ['AML.LON','AAPL']
tickers = ['DIS']

def GetAPIkey(): # get a new API key each time the script runs
    keys = "scripts/AlphaVantage/keys/keys.txt"
    lines = open(keys).read().splitlines()
    global APIkey
    APIkey = random.choice(lines)

def get_data(ticker):
    TEMPdf = pd.DataFrame()   # create empty dataframe
    print("Gather data for {}".format(ticker))
    GetAPIkey() # get a new API key each time the script runs
    ts = TimeSeries(key=APIkey, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=ticker)
    data = data[0]
    df = pd.DataFrame(data)
    df.append(data)
    ti = TechIndicators(key=APIkey, output_format='pandas')
    dataRSI = ti.get_rsi(symbol=ticker,interval=RSI_INT,time_period=RSI_PERIOD)
    dataRSI = dataRSI[0]
    TEMPdf = TEMPdf.append(dataRSI)    
    RS = TEMPdf.last('1D')
    RS = RS.iat[0,0]
    RSR = round(RS,2)
    df['11. RSI'] = RSR # add to df
    df = df.transpose()
    print(df)

for ticker in tickers:
    get_data(ticker)
