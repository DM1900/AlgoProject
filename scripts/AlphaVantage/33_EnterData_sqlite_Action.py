#!/usr/bin/python3.9
# DerekM - 2021
#
# This script write data regarding actions taken to the daily stock suggestions DB
# 

import sqlite3
from sqlite3.dbapi2 import Cursor
from datetime import datetime, timedelta

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
DB_NAME = 'pnl.db'
#DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
print("DB name: {}".format(DB_NAME))
# create table:
TABLE_DATE = "20210217_01"
TABLE_NAME = "StockData_{}".format(TABLE_DATE)
TABLE_NAME = "pldata"
print("Table name: {}".format(TABLE_NAME))
# entry_id,Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend
input("If DB & Table are correct press enter to continue...")

# read all db items
def read_table(TABLE_NAME):
    cmd = "SELECT * FROM {}".format(TABLE_NAME)
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)

#read_table(TABLE_NAME)


#def enter_data():
#    INSERT_CMD = "UPDATE StockData_20210217_01 SET Action = 'test' WHERE Ticker = 'NKE'"
#    print(INSERT_CMD)
#    cursor.execute(INSERT_CMD)
#    connection.commit()
#
#enter_data()

"""

def enter_data(TABLE_NAME,COL,TICKER,VALUE):
    #update a field
    ACTION = '"{}"'.format(ACTION)
    TICKER = '"{}"'.format(TICKER)
    INSERT_CMD = "UPDATE {} SET {} = {} WHERE {} = {}".format(TABLE_NAME,ACTION,VALUE,COL,TICKER,)
    INSERT_CMD = "UPDATE StockData_20210217_01 SET Action = 'HOLD' WHERE Ticker = 'NKE'"
    print(INSERT_CMD)
    cursor.execute(INSERT_CMD)
    connection.commit()

ACTION = "Action"
COL = "Ticker"
TICKER = "NKE"
VALUE = "Test2"
enter_data(TICKER,VALUE)

"""

# get results
#cursor.execute("SELECT * FROM pldata")
#results = cursor.fetchall()
#print(results)


def enter_data(TABLE_NAME,COLACT,VALUE,COLSRCH,TERM):
    #update a field
    VALUE = '"{}"'.format(VALUE)
    TERM = '"{}"'.format(TERM)
    INSERT_CMD = "UPDATE {} SET {} = {} WHERE {} = {}".format(TABLE_NAME,COLACT,VALUE,COLSRCH,TERM)
    #INSERT_CMD = "UPDATE StockData_20210217_01 SET Action = 'HOLD' WHERE Ticker = 'NKE'"
    print(INSERT_CMD)
    cursor.execute(INSERT_CMD)
    connection.commit()

COLACT = "Investment" # this is the column to change
VALUE = "1200" # this the value to set 'COLACT to
COLSRCH = "entry_id" # this is the search column
TERM = "49" # this is term to search in COLSRCH
enter_data(TABLE_NAME,COLACT,VALUE,COLSRCH,TERM)



# end