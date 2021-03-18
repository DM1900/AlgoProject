#!/usr/bin/python3.9
# DerekM - 2021
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

#
# create sql table
# define connection & cursor
DB_FOLDER = './scripts/db/' 
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create table:
TABLE_DATE = datetime.now().strftime("%Y%m%d_%H")
TABLE_NAME = "StockData_{}".format(TABLE_DATE)
TABLE_NAME = "StockData_20210304_22"
#TABLE_NAME = "StockData_20210215_test4"

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

# read the newly created table
def read_table(cmd):
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)
# gather all data

cmd = "SELECT * FROM {}".format(TABLE_NAME)
COL = "Suggestion"
cmd = "SELECT * FROM {} WHERE {} IN ('BUY','SELL')".format(TABLE_NAME,COL)
read_table(cmd)

#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=5min&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=RSI&symbol=AAPL&interval=daily&time_period=14&series_type=CLOSE&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=IBM&apikey=demo
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=T36W24357QF5Z698
