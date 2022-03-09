#!/usr/bin/python3.9
# DerekM - 2021

import sqlite3
from sqlite3.dbapi2 import Cursor

# define connection & cursor
DB_FOLDER = './scripts/db/' 
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

# define connection & cursor
DB_FOLDER = './scripts/db/' 
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create table:
#TABLE_DATE = "20210306_"
#TABLE_NAME = "StockData_{}".format(TABLE_DATE)
COL = "Suggestion"

def GetLastTable():
    global TABLE_NAME
    cmd = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC LIMIT 1"
    cursor.execute(cmd)
    TABLE = cursor.fetchall()
    x = TABLE[0]
    TABLE_NAME = x[0]
    print(TABLE_NAME)
    return TABLE_NAME

"""
def read_table():
    cmd = "SELECT * FROM {} WHERE {}".format(TABLE_NAME,COL)
    results = cursor.execute(cmd)
    results = results[0]
    print(results)
"""

def read_table(cmd):
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)

def main():
    GetLastTable()
    cmd = "SELECT * FROM {}".format(TABLE_NAME)
    read_table(cmd)

#VAR = input("Choose to view BUY or SELL (Leave blank for both): ") or "Both"# ask user to enter year
VAR = "*"
main()
#end