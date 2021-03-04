#!/usr/bin/python3.9
# DerekM - 2021

import sqlite3
from sqlite3.dbapi2 import Cursor

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/db/' 
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/db/' 
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create table:
TABLE_DATE = "20210304_22"
TABLE_NAME = "StockData_{}".format(TABLE_DATE)


def read_table(cmd):
    global results
    cursor.execute(cmd)
    results = cursor.fetchall()

# gather all data
cmd = "SELECT * FROM {}".format(TABLE_NAME)
#read_table(cmd)

var = input("Choose to view BUY or SELL: ") or "BUY"# ask user to enter year

# gather data from specific dates
col = "Suggestion"
#var = "BUY"
cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLE_NAME,col,var)
#print(cmd)
read_table(cmd)

#print(results)

for x in results:
    print(x)

# update a field
#cursor.execute("UPDATE pldataTEST2 SET Dividend = 999 WHERE entry_id = 4")

# delete a table
# cursor.execute("DROP TABLE IF EXISTS pldataTEST3")
# connection.commit()

# delete a row from a table
#entry_id = 53
#action = "DELETE FROM {} WHERE entry_id = {}".format(TABLE_NAME,entry_id)
#print(action)
#cursor.execute(action)
#read_table()
#connection.commit()


