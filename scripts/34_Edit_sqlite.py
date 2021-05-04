#!/usr/bin/python3.9
# DerekM - 2021 

import sqlite3
from sqlite3.dbapi2 import Cursor

# define connection & cursor
DB_FOLDER = './scripts/db/' 
DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'

DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)

cursor = connection.cursor()

# create table:
# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend,InvValue

#TABLE_NAME = "pldata"

command1 = """CREATE TABLE IF NOT EXISTS pldata (
    entry_id INTEGER PRIMARY KEY,
    Date DATE,
    TotalValue DECIMAL(16, 2),
    PieValue DECIMAL(16, 2),
    Investment DECIMAL(16, 2),
    PieInvestment DECIMAL(16, 2),
    Realised DECIMAL(16, 2),
    Dividend DECIMAL(16, 2)
)"""
#cursor.execute(command1)
#connection.commit()

# table name


TABLE_NAME = "StockData_20210430_15"

# read table
def read_table(cmd):
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)

# gather all data
cmd = "SELECT * FROM {}".format(TABLE_NAME)
#read_table(cmd)

# gather data from specific dates
col = "Ticker"
var = "AAPL"
cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLE_NAME,col,var)
#read_table(cmd)

#exit()

# Delete row from table



#n = 1_
#while n < 54:
#    print(n)
#    cmd = "SELECT * FROM {} WHERE entry_id = {}".format(TABLE_NAME,n)
#    ROW = cursor.execute(cmd).fetchone()
#    if ROW[3]is None:
#        PI = 0
#        #print("PI is (if) {}".format(PI))
#    else:
#        PI = ROW[3]
#        #print("PI is (else) {}".format(PI))
#    INV = round(float(ROW[2]) - float(PI),2)
#    cmd = "UPDATE {} SET InvValue = {} WHERE entry_id = {}".format(TABLE_NAME,INV,n)
#    print(cmd)
#    cursor.execute(cmd)
#    n = n + 1
#
#connection.commit()

# data to be entered:
#cmd = "ALTER TABLE {} ADD COLUMN {}".format(TABLE_NAME,"InvValue")
#cursor.execute(cmd)

#connection.commit() # this saves the db, without this the above entries will not be written to the db

# get results
#cursor.execute("SELECT * FROM pldata")
#results = cursor.fetchall()
#print(results)

# update a field
#cursor.execute("UPDATE pldataTEST2 SET Dividend = 999 WHERE entry_id = 4")

# delete a table
#TABLE_NAME = "StockData_20210430_15"
#cursor.execute("DROP TABLE IF EXISTS {}".format(TABLE_NAME))
#connection.commit()
