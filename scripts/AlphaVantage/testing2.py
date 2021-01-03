print("Start")
print("Load packages")
import pandas
from alpha_vantage.timeseries import TimeSeries
import sys
import random
import time

#variables
WAITTIME = 3

print
tickerlist = "tickers/AV/tickerfile_TRADELIST.txt"
tickerlist = "tickers/AV/tickerfile_TEST.txt"
tickerlist = "tickers/AV/tickerfile_TEST_USA.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

def GetAPIkey():
    print("Get API Key")
    keys = "scripts/AlphaVantage/keys.txt"
    lines = open(keys).read().splitlines()
    global APIkey
    APIkey = random.choice(lines)

def get_data(ticker):
    print(ticker)
    GetAPIkey() # get a new API key each time the script runs
    ts = TimeSeries(key=APIkey, output_format='pandas')
    data, meta_data = ts.get_quote_endpoint(symbol=ticker);
    print(data)
    print("wait...")
    time.sleep(WAITTIME)

print("get_data has been set, running it now...")
for ticker in tickers:
    get_data(ticker)


#https://www.alphavantage.co/query?function=TimeSeries&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698