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
import sqlite3
from sqlite3.dbapi2 import Cursor

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

# create sql table
# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create table:
TABLE_DATE = datetime.now().strftime("%Y%m%d_%H")
TABLE_NAME = "StockData_{}".format(TABLE_DATE)
#TABLE_NAME = "StockData_20210215_test4"

command1 = """CREATE TABLE IF NOT EXISTS {} (
    entry_id INTEGER PRIMARY KEY,
    Date DATE,
    Ticker TEXT,
    Price DECIMAL(16, 2),
    PreviousClose DECIMAL(16, 2),
    Change TEXT,
    RSI DECIMAL(4, 2),
    Suggestion TEXT,
    Action TEXT
)""".format(TABLE_NAME)


#cursor.execute(command1)
#print(command1)
cursor.execute(command1)
connection.commit()
#
#INSERT_CMD = "INSERT INTO StockData_20210215_test3 VALUES (NULL,0,0,0,0,0,0,0,0)"
#print(INSERT_CMD)
#cursor.execute(INSERT_CMD)
#connection.commit()

#INSERT_CMD = "INSERT INTO {} VALUES (NULL,NULL,0,1,2,3,4,5,6)".format(TABLE_NAME)
#INSERT_CMD = "INSERT INTO StockData_20210215_test3 VALUES (NULL,15/02/2021,AAPL,135.3700,135.1300,0.1776,52.97,NULL,NULL)"
#INSERT_CMD = "INSERT INTO StockData_20210215_test3 VALUES (NULL,15/02/2021,'AAPL',135.3700,135.1300,0.1776,52.97,NULL,NULL)"
#print(INSERT_CMD)
#cursor.execute(INSERT_CMD)
#connection.commit()
#exit()
#
# Set variables
DDATE = datetime.now().strftime("%d/%m/%Y")
Date = '"{}"'.format(DDATE)
DDATE = '"{}"'.format(DDATE)
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
HOLD = "HOLD"
# how long to wait between API calls (kind of irrelevant due to the way Alpha Vantage limits calls, but anyway...)
WAITAPI = 5
WAITERR = 5
#
# list of alpha vantage keys
keys = "/home/admin/AlgoProject/scripts/AlphaVantage/keys/keys.txt" 
#
# this is the mian one with all tickers
tickerlist = "tickerfile_TRADELIST.txt" # main list of all selected tickers
#tickerlist = "tickerfile_TEST.txt"
#tickerlist = "tickerfile_TEST_USA.txt"
#
tickerlist = "tickers/AV/{}".format(tickerlist)
#
logging.info(tickerlist)
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

#tickers = ['AAPL']


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
        DCHANGE = 0
        while SUCCESS < 10:
            try:
                GetAPIkey() # get a new API key each time the script runs
                ts = TimeSeries(key=APIkey, output_format='pandas')
                data = ts.get_quote_endpoint(symbol=ticker)#;
                TEMPdf = df.append(data)
                DTICKER = TEMPdf.iat[0,0]
                DTICKER = '"{}"'.format(DTICKER)
                print("Getting data for {}".format(DTICKER))
                print(DTICKER)
                DPRICE = TEMPdf.iat[0,4]
                print(DPRICE)
                DCLOSE = TEMPdf.iat[0,7]
                print(DCLOSE)
                DCHANGE = TEMPdf.iat[0,9]
                DCHANGE = '"{}"'.format(DCHANGE)
                print(DCHANGE)
                TEMPdf = pd.DataFrame() # create empty dataframe
                SUCCESS=True
                break
            except:
                logging.exception("{} - Price exception".format(ticker))
                SUCCESS=SUCCESS + 1
                logging.debug("{} - Error found, {}, attempt no. {}. ({})".format(DCHANGE, DCHANGE, SUCCESS, APIkey))
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
                #print(RS)
                RSR = round(RS,2)
                #print(RSR)
                #df['RSI'] = RSR
                # suggest buy/sell based on RSI & price action
                if  RS > RSIVHIGH: 
                    SUGGESTION = SELL
                elif RS < RSIVLOW:
                    SUGGESTION = BUY
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
                SUGGESTION = '"{}"'.format(SUGGESTION)
                #print(SUGGESTION)
                #df2 = df2.append(df)
                break
                #logging.info(df2)
            except:
                logging.exception("{} - RSI exception".format(ticker))
                SUCCESS=SUCCESS + 1
                logging.debug("{} - Error found, {}, attempt no. {}. ({})".format(ticker, "RSI", SUCCESS, APIkey))
                time.sleep(WAITERR)
        INSERT_CMD = "INSERT INTO {} VALUES (NULL,{},{},{},{},{},{},{},NULL)".format(TABLE_NAME,DDATE,DTICKER,DPRICE,DCLOSE,DCHANGE,RSR,SUGGESTION)
        print("Print INSERT_CMD")
        print(INSERT_CMD)
        cursor.execute(INSERT_CMD)
        connection.commit()
    except: # catch all exceptions in the same way
        logging.exception("Main Error catch")
        logging.info("{} - Error found, {}, attempting to continue...".format(ticker, "Main Error catch"))

try:
    logging.info("get_data has been set, running it now...")
    for ticker in tickers:
        get_data(ticker)
except: # catch all exceptions in the same way
    logging.exception("Error running get_data loop")
    #logging.info("Error")


# read the newly created table
def read_table(cmd):
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)
# gather all data
cmd = "SELECT * FROM {}".format(TABLE_NAME)
#read_table(cmd)

# finish up
# #df2 = df2.read_csv(CSV_FILE)
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
