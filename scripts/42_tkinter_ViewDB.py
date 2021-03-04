#!/usr/bin/python3.9
# DerekM - 2021

import tkinter as tk
#from tkinter import ttk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle 
from ttkthemes import ThemedTk
import sys
import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from typing import Text

"""
window = ThemedTk(theme="itft1")
ttk.Button(window, text="Quit", command=window.destroy).pack()
window.mainloop()

#greeting = tk.Label(text="Hello, Tkinter")
greeting = ThemedTk(theme="itft1")
#greeting.pack()
ttk.Button(greeting,text="Click me!").pack()
greeting.mainloop()
"""


# change theme:
#s = ttk.Style()
#s.theme_use('alt')
#s.theme_use('clam')

#themes = s.theme_use()
#print(themes)

# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/db/' 
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
    print(results)

def get_data(DATA):
    global DENTRYID, DDATE,DTOTAL,DPIE,DINV,DPIEINV,DREAL,DDIV,DVAL,DPER,DPIV 
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
    #DPIV = round((((DPIE / DPIEINV)-1)*100) ,1)

# gather data for specific year
YEAR = input("Choose year to gather data for (leave blank to gather all data): ") or "0" # ask user to enter year

if YEAR == "0":
    col = "entry_id"
    cmd = 'SELECT * FROM {} ORDER BY {} DESC LIMIT 1'.format(TABLE_NAME,col) # Get all data
    read_table(cmd)
    DATA = results[0]
    print(DATA)
    get_data(DATA)
elif YEAR == "2020":
    col = "Date"
    var = YEAR
    cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
    print(cmd)
    read_table_year(cmd,var)
    # set data values:
    DATA = results[0]
    print(DATA)
    get_data(DATA)
else:#  YEAR == "2021":
    # get data for last year
    LAST_YEAR = int(YEAR) - 1
    col = "Date"
    var = LAST_YEAR
    cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
    print(cmd)
    read_table_year(cmd,var)
    DATA = results[0]
    print(DATA)
    get_data(DATA)
    # get data for thi year   
    #col = "Date"
    var = YEAR
    cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%' ORDER BY entry_id DESC LIMIT 1".format(TABLE_NAME,col,var) # get data from 1 year
    print(cmd)
    read_table_year(cmd,var)
    LYPROF = (DTOTAL - DPIE) - DINV
    DATA = results[0]
    DENTRYID = DATA[0]
    DDATE = DATA[1]
    DTOTAL = DATA[2] # Total account value
    #DPIE = DATA[3] - DPIE
    DINVO = DINV # This is the total amount actually lodged to the account
    DINV = DATA[4] + LYPROF # Total amount invested plus profit from last year
    #DPIEINV = DATA[5] - DPIEINV
    DREAL = DATA[6] - DREAL # amount realised this calendar year
    DDIV = DATA[7] - DDIV # dividend received this calendar year
    DVAL = DATA[8] 
    DPER = round((((DVAL / DINV)-1)*100) ,1)
    #DPIV = round((((DPIE / DPIEINV)-1)*100) ,1)

TEXT = """Total value of account is €{}
{} stats:
Realised value is €{}
Diviend recieved is €{}
Stock value is €{}
Investment value is €{}
Stock value increase is {}%""".format(DTOTAL,YEAR,DREAL,DDIV,DVAL,DINV,DPER)
print(TEXT)

exit()

###
print("Try to create tkinter window")

#window = ThemedTk(theme="itft1")
#ttk.Button(window, text="Quit", command=window.destroy).pack()
#window.mainloop()

#window = tk.Tk()
style = "clam"
style = "black"
style = "alt"
style = "breeze"
#style = "blue"
#style = "equilux"
style = "default"
#style = "aqua"

window = ThemedTk(theme=style)
info = "Account Data {}".format(DDATE)
window.title(info)
window.geometry('300x300')

frame_a = ttk.Frame()
frame_b = ttk.Frame()
frame_c = ttk.Frame()

TEXT = """Total value of account is €{}
Realised value is €{}
Diviend recieved is €{}""".format(DTOTAL,DREAL,DDIV)
ttk.Label(master=frame_a, text=TEXT).grid(column=0,row=0)

TEXT = """Stock value is €{}
Stock investment is €{}
Stock value increase is {}%""".format(DVAL,DINV,DPER)
ttk.Label(master=frame_b, text=TEXT).pack()

TEXT = """Pie value is €{}
Pie investment is €{}
Pie value increase is {}%""".format(DPIE,DPIEINV,DPIV)
ttk.Label(master=frame_c, text=TEXT).pack()


frame_a.pack()
frame_b.pack()
frame_c.pack()


def call_script():
    print("Create chart")
    pycmd = 'python scripts/41_VisualiseData.py'
    os.system(pycmd)


#script = "python scripts/41_VisualiseData.py"
ttk.Button(window, text="Create Chart", command=call_script).pack()

ttk.Button(window, text="Quit", command=window.destroy).pack()

window.mainloop()

#exit()




exit()






# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/db/' 
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
var = "2021"
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


