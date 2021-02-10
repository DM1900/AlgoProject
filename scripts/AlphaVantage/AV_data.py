#!/usr/bin/python3.9
# DerekM - 2021
# The data is gathered from Alpha Vantage which has a delay of 1 day on all stock data.
# Please factor that into any tradng decisions (this is based on Daily RSI so it's not such a big issue here)
#
# imports:
import logging
from datetime import datetime, timedelta
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators 
import sys
import random
import time
import csv
# Logging variables
logfile = datetime.now().strftime("%Y%m%d-%H%M")
logfile = "logs/AV_log_{}.log".format(logfile)
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.DEBUG)

# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logfile,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)
#
logging.info(datetime.now())
logging.info("Starting AlphaVantage data script")

# variables
logging.info("Set variables")
#
START = datetime.now()
logging.info(START)
#
RSI_PERIOD = 14 # no. of days to calculate RSI
RSI_INT = 'daily' # interval to calculate RSI
# RSI values
RSIVLOW = 20
RSILOW = 45
RSIHIGH = 65
RSIVHIGH = 80
logging.info("RSI settings: Period: {} days, Low: {}, High {}".format(RSI_PERIOD,RSILOW,RSIHIGH))
# RSI Suggestions
BUY = "BUY"
BUYRSI = "BUY (RSI very low)"
SELL = "SELL"
SELLRSI = "SELL (RSI very high)"
HOLD = "-"
#
WAITAPI = 3
WAITERR = 8
#
keys = "scripts/AlphaVantage/keys/keys.txt" # list of alpha vantage keys
#
tickerlist = "tickerfile_TRADELIST.txt" # this is the mian one with all tickers
#tickerlist = "tickerfile_TEST.txt"
#tickerlist = "tickerfile_TEST_USA.txt"
#
tickerlist = "tickers/AV/{}".format(tickerlist)
logging.info(tickerlist)
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

def GetAPIkey(): # get a new API key each time the script runs
    try:
        #logging.info("Get API Key")
        lines = open(keys).read().splitlines()
        global APIkey
        APIkey = random.choice(lines)
        #logging.info("Got API key, {key}, now waiting to continue...".format(key = APIkey))
        time.sleep(WAITAPI)
    except:
        logging.exception("Error getting API key")
        #time.sleep(WAITERR)

df2 = pd.DataFrame(columns=[])  # create empty dataframe
logging.info(datetime.now())

def get_data(ticker):
    try:
        # create empty dataframes
        TEMPdf = pd.DataFrame()
        df = pd.DataFrame()
        global df2
        logging.info(ticker)
        # Price data
        logging.info("Get price data")
        SUCCESS = 0
        while SUCCESS < 10:
            try:
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
                SUCCESS=True
                break
            except:
                logging.exception("{} - Price exception".format(ticker))
                SUCCESS=SUCCESS + 1
                logging.debug("{} - Error found, {}, attempt no. {}. ({})".format(ticker, "Price", SUCCESS, APIkey))
                time.sleep(WAITERR)
        # RSI data
        logging.info("Get RSI data")
        #SUCCESS = 0
        while SUCCESS < 10:
            try:
                GetAPIkey() # get a new API key each time the script runs
                ti = TechIndicators(key=APIkey, output_format='pandas')
                dataRSI = ti.get_rsi(symbol=ticker,interval=RSI_INT, time_period=RSI_PERIOD)
                dataRSI = dataRSI[0]
                TEMPdf = TEMPdf.append(dataRSI)
                RS = TEMPdf.last('1D')
                RS = RS.iat[0,0]
                RSR = round(RS,2)
                df['RSI'] = RSR
                # suggest buy/sell based on RSI & price action
                if  RS > RSIVHIGH: 
                    SUGGESTION = SELLRSI
                elif RS < RSIVLOW:
                    SUGGESTION = BUYRSI
                elif  RS > RSIHIGH: 
                    if DCLOSE > DPRICE:
                        SUGGESTION = SELL
                    else:
                        SUGGESTION = HOLD
                elif RS < RSILOW:
                    if DCLOSE < DPRICE:
                        SUGGESTION = BUY
                    else:
                        SUGGESTION = HOLD
                else:
                    SUGGESTION = HOLD
                df['Suggestion'] = SUGGESTION
                df2 = df2.append(df)
                break
                #logging.info(df2)
            except:
                logging.exception("{} - RSI exception".format(ticker))
                SUCCESS=SUCCESS + 1
                logging.debug("{} - Error found, {}, attempt no. {}. ({})".format(ticker, "RSI", SUCCESS, APIkey))
                time.sleep(WAITERR)
    except: # catch all exceptions in the same way
        logging.exception("Main Error catch")
        logging.info("{} - Error found, {}, attempting to continue...".format(ticker, "Main Error catch"))
try:
    logging.info("get_data has been set, running it now...")
    for ticker in tickers:
        get_data(ticker)

    #df2 = df2.sort_values(by=['Ticker'])
    df2 = df2.sort_values(by=['Suggestion','RSI'], ascending=False)
    logging.info("PRINT df2")
    logging.info(df2)

    logging.info("Write 'df2' to csv")
    CSV_FILE = datetime.now().strftime('scripts/AlphaVantage/output/AVData_%Y%m%d.csv')
    df2.to_csv(CSV_FILE,index=False)
except: # catch all exceptions in the same way
    logging.exception("Error running get_data loop")
    #logging.info("Error")

#df2 = df2.read_csv(CSV_FILE)
FINISH = datetime.now()
logging.info(FINISH)
TIMETAKEN = FINISH - START
logging.info("Time taken to run the script: {}".format(TIMETAKEN))
logging.info("End")

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=CLOSE&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=T36W24357QF5Z698
