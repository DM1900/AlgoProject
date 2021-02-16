import sqlite3
from sqlite3.dbapi2 import Cursor

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)

cursor = connection.cursor()
# delete a table
NUM = 2020
TABLE_NAME = "StockData_20210215_{}".format(NUM)
#TABLE_NAME = "pldataTEST"
#TABLE_NAME = "StockData_20210215_test4"

cmd = "DROP TABLE IF EXISTS {}".format(TABLE_NAME)
cursor.execute(cmd)
connection.commit()
