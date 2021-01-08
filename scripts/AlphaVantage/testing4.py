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
RSI_INT = 'daily' # interval to calculate RSI
RSIVLOW = 10
RSILOW = 45
RSIHIGH = 65
RSIVHIGH = 90
BUY = "BUY"
SELL = "SELL"
HOLD = "-"
###
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
WAITTIME = 10

tickerlist = "tickers/AV/tickerfile_TRADELIST.txt"
#tickerlist = "tickers/AV/tickerfile_TEST.txt"
#tickerlist = "tickers/AV/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

def GetAPIkey(): # get a new API key each time the script runs
    #print("Get API Key")
    keys = "scripts/AlphaVantage/keys/keys.txt"
    lines = open(keys).read().splitlines()
    global APIkey
    APIkey = random.choice(lines)
    print("Got API key, {key}, now waiting to continue...".format(key = APIkey))
    time.sleep(WAITTIME)

df2 = pd.DataFrame(columns=[])  # create empty dataframe

def get_data(ticker):
    # add error catching!!!she
    TEMPdf = pd.DataFrame()   # create empty dataframe
    df = pd.DataFrame()   # create empty dataframe
    global df2
    print(ticker)
    GetAPIkey() # get a new API key each time the script runs
    ts = TimeSeries(key=APIkey, output_format='pandas')
    data = ts.get_quote_endpoint(symbol=ticker)#;
    TEMPdf = df.append(data)
    DTICKER = TEMPdf.iat[0,0]
    df = df.append({'Ticker':DTICKER}, ignore_index=True) # add to df
    DPRICE = TEMPdf.iat[0,4]
    df['Price'] = DPRICE # add to df
    DCLOSE = TEMPdf.iat[0,7]
    df['PreviousClose'] = DCLOSE # add to df
    DCHANGE = TEMPdf.iat[0,9]
    df['Change(%)'] = DCHANGE # add to df
    TEMPdf = pd.DataFrame() # create empty dataframe
    # get RSI data using a new VA API key
    GetAPIkey() # get a new API key each time the script runs
    ti = TechIndicators(key=APIkey, output_format='pandas')
    dataRSI = ti.get_rsi(symbol=ticker,interval=RSI_INT, time_period=RSI_PERIOD)
    dataRSI = dataRSI[0]
    TEMPdf = TEMPdf.append(dataRSI)
    RS = TEMPdf.last('1D')
    RS = RS.iat[0,0]
    RSR = round(RS,1)
    df['RSI'] = RSR
    # suggest buy/sell based on RSI & price action
    if  RS > RSIVHIGH:
        df['Suggestion'] = SELL
    elif RS < RSIVLOW:
        df['Suggestion'] = BUY
    elif  RS > RSIHIGH: 
        if DCLOSE > DPRICE:
            df['Suggestion'] = SELL
        else:
            df['Suggestion'] = HOLD
    elif RS < RSILOW:
        if DCLOSE < DPRICE:
            df['Suggestion'] = BUY
        else:
            df['Suggestion'] = HOLD
    else:
        df['Suggestion'] = HOLD
    df2 = df2.append(df)
    #print(df2)

print("get_data has been set, running it now...")
for ticker in tickers:
    try:
        get_data(ticker)
    except: # catch all exceptions in the same way
        err = sys.exc_info()[0]
        print(err)
        print("{} - Error found, attempting to continue...".format(ticker))
    #finally:
    #    print("Conituning...")

print("PRINT df2")
print(df2)

print("Write 'df2' to csv")
CSV_FILE = datetime.now().strftime('scripts/AlphaVantage/output/AVData_%Y%m%d.csv')
df2.to_csv(CSV_FILE,index=False)

print(datetime.now())

#https://www.alphavantage.co/query?function=TimeSeries&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=CLOSE&apikey=T36W24357QF5Z698

