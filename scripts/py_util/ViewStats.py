#!/usr/bin/python3.9
# DerekM - 2021

import sys
import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from typing import Text

# define connection & cursor
DB_FOLDER = './scripts/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

TABLE_NAME = "pldata"
#TABLE_NAME = "pldataTEST3"

# set global variables:

def read_table(cmd):
    global results
    cursor.execute(cmd)
    results = cursor.fetchall()

def read_table_year(cmd,var):
    global results
    cursor.execute(cmd)
    results = cursor.fetchall()    

def get_data(DATA):
    global DENTRYID, DDATE,DTOTAL,DPIE,DINV,DPIEINV,DREAL,DDIV,DVAL,DPER 
    DENTRYID = DATA[0]
    DDATE = DATA[1]
    DTOTAL = DATA[2]
    DPIE = DATA[3]
    DINV = DATA[4]
    DPIEINV = DATA[5]
    DREAL = DATA[6]
    DDIV = DATA[7]
    DVAL = DATA[8]
    DPER = round((((DVAL / DINV)-1)*100) ,1)

def Get_Stats(YEAR):
    global TEXT
    if YEAR == 0:
        YEAR = "ALL"
        col = "entry_id"
        cmd = 'SELECT * FROM {} ORDER BY {} DESC LIMIT 1'.format(TABLE_NAME,col) # Get all data
        read_table(cmd)
        DATA = results[0]
        #print(DATA)
        get_data(DATA)
    elif int(YEAR) < int(2020):
        print("Invalid year: {}".format(YEAR))
        exit()
    elif int(YEAR) > int(2021):
        print("Invalid year: {}".format(YEAR))
        exit()
    elif YEAR == 2020:
        col = "Date"
        var = YEAR
        cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
        #print(cmd)
        read_table_year(cmd,var)
        # set data values:
        DATA = results[0]
        #print(DATA)
        get_data(DATA)
    else:#  YEAR == "2021":
        # get data for last year
        LAST_YEAR = int(YEAR) - 1
        col = "Date"
        var = LAST_YEAR
        cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
        #print(cmd)
        read_table_year(cmd,var)
        DATA = results[0]
        #print(DATA)
        get_data(DATA)
        # get data for thi year   
        #col = "Date"
        var = YEAR
        cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
        #print(cmd)
        read_table_year(cmd,var)
        global DENTRYID, DDATE,DTOTAL,DPIE,DINV,DPIEINV,DREAL,DDIV,DVAL,DPER 
        LYPROF = (DTOTAL - DPIE) - DINV
        DATA = results[0]
        DENTRYID = DATA[0]
        DDATE = DATA[1]
        DTOTAL = DATA[2] # Total account value
        #DPIE = DATA[3] - DPIE
        #DINVO = DINV # This is the total amount actually lodged to the account
        DINV = DATA[4] + LYPROF # Total amount invested plus profit from last year
        #DPIEINV = DATA[5] - DPIEINV
        DREAL = round(DATA[6] - DREAL,2) # amount realised this calendar year
        DDIV = round(DATA[7] - DDIV,2) # dividend received this calendar year
        DVAL = DATA[8] 
        DPER = round((((DVAL / DINV)-1)*100) ,1)
        #DPIV = round((((DPIE / DPIEINV)-1)*100) ,1)

    TEXT = """{} stats ({}):
    Total value of account is €{}
    Realised value is €{}
    Dividend recieved is €{}
    Stock value is €{}
    Investment value is €{}
    Stock value increase is {}%""".format(YEAR,DDATE,DTOTAL,DREAL,DDIV,DVAL,DINV,DPER)
    
    return TEXT


# gather data for specific year
#YEAR = int(input("Choose year to gather data for (leave blank to gather all data): ") or 0 )# ask user to enter year

#Get_Stats(2020)
#print(TEXT)


###
