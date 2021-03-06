#!/usr/bin/python3.9
# DerekM - 2021

import tkinter as tk
#from tkinter import ttk
import tkinter.ttk as ttk
from ttkthemes import ThemedStyle 
from ttkthemes import ThemedTk

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
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

TABLE_NAME = "pldata"
#TABLE_NAME = "pldataTEST3"

def read_table(cmd):
    global results
    cursor.execute(cmd)
    results = cursor.fetchall()
    
# gather data from specific dates
col = "entry_id"
cmd = 'SELECT * FROM {} ORDER BY {} DESC LIMIT 1'.format(TABLE_NAME,col)

read_table(cmd)
DATA = results[0]
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
DPIV = round((((DPIE / DPIEINV)-1)*100) ,1)
###
print("Try to create tkinter window")

window = ThemedTk(theme="itft1")
ttk.Button(window, text="Quit", command=window.destroy).pack()
window.mainloop()

#window = tk.Tk()
info = "Account Data {}".format(DDATE)
window.title(info)

frame_a = ttk.Frame()
frame_b = ttk.Frame()
frame_c = ttk.Frame()

TEXT = """Total value of account is €{}
Realised value is €{}
Diviend recieved is €{}""".format(DTOTAL,DREAL,DDIV)
label_a = tk.Label(master=frame_a, text=TEXT)
label_a.pack()

TEXT = """Stock value is €{}
Stock investment is €{}
Stock value increase is {}%""".format(DVAL,DINV,DPER)
label_b = tk.Label(master=frame_b, text=TEXT)
label_b.pack()

TEXT = """Pie value is €{}
Pie investment is €{}
Pie value increase is {}%""".format(DPIE,DPIEINV,DPIV)
label_c = tk.Label(master=frame_c, text=TEXT)
label_c.pack()


frame_a.pack()
frame_b.pack()
frame_c.pack()

window.mainloop()

#exit()




exit()






# define connection & cursor
DB_FOLDER = '/home/admin/AlgoProject/scripts/AlphaVantage/db/' 
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

