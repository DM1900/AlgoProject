#!/usr/bin/python3.9
# DerekM - 2021

import sqlite3
from sqlite3.dbapi2 import Cursor
from datetime import datetime, timedelta

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# entry_id,Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

TABLE_NAME = "pldata"
LASTROW = cursor.execute('SELECT * FROM pldata ORDER BY entry_id DESC LIMIT 1').fetchone()
TABLEDATE = LASTROW[1]

DATE = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 

def enter_data():
    DATE = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 
    print("Enter data for {}".format(DATE))
    TotalValue = float(input("Enter total account value: "))
    PieValue = float(input("Enter Pie value: "))
    #Investment = input("Enter invested amount: ") 
    tmp = float(LASTROW[4])
    print("Invested amount is €{}, any change?: ".format(tmp))
    Investment = float(input("Enter additional ammount here or leave blank: ") or "0")
    Investment = float(tmp) + Investment
    tmp = float(LASTROW[5])
    print("Pie Invested amount is €{}, any change?: ".format(tmp))
    PieInvestment = float(input("Enter additional ammount here or leave blank: ") or "0")
    PieInvestment = tmp + PieInvestment
    tmp = LASTROW[6]
    Realised = input("Enter Realised value (current value €{}): ".format(tmp))
    if Realised == "":
        Realised = tmp
    tmp = LASTROW[7]
    Dividend = input("Enter Dividend value received (current value €{}): ".format(tmp))
    if Dividend == "":
        Dividend = tmp
    DATE = '"{}"'.format(DATE)
    InvValue = TotalValue - PieInvestment
    INSERT_CMD = "INSERT INTO pldata VALUES (NULL,{},{},{},{},{},{},{},{})".format(DATE,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend,InvValue)
    print(INSERT_CMD)
    cursor.execute(INSERT_CMD)
    connection.commit()

if DATE == TABLEDATE:
    print("Date conflict")
    CONTINUE = input("Date ({}) already assigned, do you wish to continue? (y or n)".format(DATE)) 
    if CONTINUE == "y":
        enter_data()
    else:
        print("No action taken, end of script")
        print("Existing data: {}".format(LASTROW))
else:
    enter_data()

# get results
#cursor.execute("SELECT * FROM pldata")
#results = cursor.fetchall()
#print(results)

# end