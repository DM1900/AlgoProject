#!/usr/bin/python3.9
# DerekM - 2021

import sqlite3
from sqlite3.dbapi2 import Cursor

# define connection & cursor
DB_FOLDER = './scripts/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

TABLE_NAME = "pldata"
#TABLE_NAME = "pldataTEST3"

def read_table(cmd):
    cursor.execute(cmd)
    results = cursor.fetchall()
    print(results)

# gather all data
cmd = "SELECT * FROM {}".format(TABLE_NAME)
#read_table(cmd)

# gather data from specific dates
col = "Date"
var = "2020"
cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLE_NAME,col,var)
read_table(cmd)


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


