#!/usr/bin/python3
# DerekM - 2021
# The data is gathered from Alpha Vantage which has a delay of 1 day on all stock data.
# Please factor that into any tradng decisions (this is based on Daily RSI so it's not such a big issue here)
#

# imports:
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
# custom functions
from py_util import AV_func
from py_util import SQLITE_func
from py_util import pylog as log

# relative path, it's up to you which one to use:
RPATH = "."
RPATH = "/home/admin/AlgoProject"

# Log variables:
LOGTIME = datetime.now().strftime("%Y%m%d-%H")
LOGFILE = "{}/logs/".format(RPATH)
LOGFILE = LOGFILE + "Log_{}.log".format(LOGTIME)

START = datetime.now()
SCRIPTNAME = "'02_get_data_sqlite.py'"

def LogTest(logfile,msg):
    msg = "{} {}".format(LOGTIME,msg)
    f = open(logfile, "a")
    f.write("""{}
""".format(msg))
    f.close()
TESTTEXT = "{} Run confirmation from python script ('02_get_data_sqlite.py')".format(START)
LogTest(LOGFILE,TESTTEXT)

# relative path, it's up to you which one to use:
RPATH = "."
RPATH = "/home/admin/AlgoProject"

# Log variables:
LOGTIME = datetime.now().strftime("%Y%m%d-%H")
LOGFILE = "{}/logs/".format(RPATH)
LOGFILE = LOGFILE + "Log_{}.log".format(LOGTIME)

START = datetime.now()
SCRIPTNAME = "'02_get_data_sqlite.py'"

#MESSAGE = "Log Test: {}, {}, {}".format(START,LOGFILE,SCRIPTNAME)
#log.WriteToLog(LOGFILE,MESSAGE)

log.WriteToLog(LOGFILE,"Starting {} script at {}".format(SCRIPTNAME,START))
#
# create sql table
# define connection & cursor
DB_FOLDER = '{}/scripts/db/'.format(RPATH)
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create table:
TABLE_DATE = datetime.now().strftime("%Y%m%d_%H")
TABLE_NAME = "StockData_{}".format(TABLE_DATE)
#TABLE_NAME = "StockData_20210215_test4"
log.WriteToLog(LOGFILE,"{} {}".format(DB_NAME,TABLE_NAME))
# Create new Database Table
SQLITE_func.CreateDB(DB_NAME,TABLE_NAME)

# Set variables
DDATE = datetime.now().strftime("%d/%m/%Y")
Date = '"{}"'.format(DDATE)
DDATE = '"{}"'.format(DDATE)
#
RSI_PERIOD = 14 # no. of days to calculate RSI
RSI_INT = 'daily' # interval to calculate RSI
# RSI values, these are used to determine buy/sell suggestions
RSIVLOW = 20
RSILOW = 35
RSIHIGH = 70
RSIVHIGH = 80
log.WriteToLog(LOGFILE,"RSI settings: Period: {} days, Low: {}, High {}".format(RSI_PERIOD,RSILOW,RSIHIGH))
# RSI Suggestions
BUY = "BUY"
#BUYRSI = "BUY (RSI very low)"
SELL = "SELL"
#SELLRSI = "SELL (RSI very high)"
HOLD = "HOLD"
# how long to wait between API calls (kind of irrelevant due to the way Alpha Vantage limits calls, but anyway...)
WAITAPI = 7
WAITERR = 5
#
# list of alpha vantage keys
KEYS = "{}/scripts/keys/keys.txt".format(RPATH)
#
# this is the mian one with all tickers
log.WriteToLog(LOGFILE,"Set ticker list")
tickers = "tickerfile_TRADELIST.txt" # main list of all selected tickers
#tickers = "tickerfile_TEST.txt"
#tickers = "tickerfile_TEST_USA.txt"
#
tickerlist = "{}/tickers/AV/{}".format(RPATH,tickers)
#
log.WriteToLog(LOGFILE,tickerlist)
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]

#tickers = ['AAPL']


df2 = pd.DataFrame(columns=[])  # create empty dataframe

def get_data(ticker):
    try:
        print("Processing data for {}".format(ticker))
        # create empty dataframes
        TEMPdf = pd.DataFrame()
        df = pd.DataFrame()
        global df2
        #log.WriteToLog(LOGFILE,ticker)
        # Price data
        SUCCESS = 0
        DCHANGE = 0
        while SUCCESS < 10:
            try:
                APIkey = AV_func.GetAPIkey(KEYS) # get a new API key each time the script runs
                time.sleep(WAITAPI)
                ts = TimeSeries(key=APIkey, output_format='pandas')
                data = ts.get_quote_endpoint(symbol=ticker)#;
                TEMPdf = df.append(data)
                DTICKER = TEMPdf.iat[0,0]
                DTICKER = '"{}"'.format(DTICKER)
                log.WriteToLog(LOGFILE,"Getting data for {}".format(DTICKER))
                DPRICE = TEMPdf.iat[0,4]
                DCLOSE = TEMPdf.iat[0,7]
                DCHANGE = TEMPdf.iat[0,9]
                DCHANGE = '"{}"'.format(DCHANGE)
                TEMPdf = pd.DataFrame() # create empty dataframe
                SUCCESS=True
                break
            except:
                log.WriteToLog(LOGFILE,"{} - Price exception".format(ticker))
                SUCCESS=SUCCESS + 1
                log.WriteToLog(LOGFILE,"{} - Error found, {}, attempt no. {}. ({})".format(DCHANGE, DCHANGE, SUCCESS, APIkey))
                time.sleep(WAITERR)
        # RSI data
        log.WriteToLog(LOGFILE,"Get RSI data for {}".format(DTICKER))
        #SUCCESS = 0
        while SUCCESS < 10:
            try:
                APIkey = AV_func.GetAPIkey(KEYS) # get a new API key each time the script runs
                time.sleep(WAITAPI)
                ti = TechIndicators(key=APIkey, output_format='pandas')
                dataRSI = ti.get_rsi(symbol=ticker,interval=RSI_INT, time_period=RSI_PERIOD)
                dataRSI = dataRSI[0]
                TEMPdf = TEMPdf.append(dataRSI)
                RS = TEMPdf.last('1D')
                RS = RS.iat[0,0]
                RSR = round(RS,2)
                # suggest buy/sell based on RSI & price action
                # #def GetSuggestion(RS,DCLOSE,DPRICE,BUY,SELL,HOLD,RSIHIGH,RSIVHIGH,RSILOW,RSIVLOW):
                SUGGESTION = AV_func.GetSuggestion(RS,DCLOSE,DPRICE,BUY,SELL,HOLD,RSIHIGH,RSIVHIGH,RSILOW,RSIVLOW)
                SUGGESTION = '"{}"'.format(SUGGESTION)
                #log.WriteToLog(LOGFILE,"Suggestion for {}: {}".format(ticker,SUGGESTION))
                #df2 = df2.append(df)
                break
                #logging.info(df2)
            except:
                log.WriteToLog(LOGFILE,"{} - RSI exception".format(ticker))
                SUCCESS=SUCCESS + 1
                log.WriteToLog(LOGFILE,"{} - Error found, {}, attempt no. {}. ({})".format(ticker, "RSI", SUCCESS, APIkey))
                time.sleep(WAITERR)
        INSERT_CMD = "INSERT INTO {} VALUES (NULL,{},{},{},{},{},{},{},NULL)".format(TABLE_NAME,DDATE,DTICKER,DPRICE,DCLOSE,DCHANGE,RSR,SUGGESTION)
        log.WriteToLog(LOGFILE,INSERT_CMD)
        cursor.execute(INSERT_CMD)
        connection.commit()
    except: # catch all exceptions in the same way
        log.WriteToLog(LOGFILE,"Main Error catch {}".format(ticker))
        log.WriteToLog(LOGFILE,"{} - Error found, {}, attempting to continue...".format(ticker, "Main Error catch"))

try:
    log.WriteToLog(LOGFILE,"get_data has been set, running it now...")
    for ticker in tickers:
        get_data(ticker)
except: # catch all exceptions in the same way
    log.WriteToLog(LOGFILE,"Error running get_data loop")


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
log.WriteToLog(LOGFILE,FINISH)
TIMETAKEN = FINISH - START
log.WriteToLog(LOGFILE,"Time taken to run the script: {}".format(TIMETAKEN))
log.WriteToLog(LOGFILE,"END")

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=CLOSE&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=T36W24357QF5Z698
