import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
#plt.close("all")
# plot style

style = 'fivethirtyeight'
style = 'ggplot'
style = 'fast'
style = 'seaborn'
style = 'seaborn-whitegrid'

plt.style.use(style)

# Create your connection.
DB_FOLDER = './scripts/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
print(DB_NAME)
TABLE_NAME = "pldata"
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# create datastore with data from db
cmd = "SELECT * FROM {}".format(TABLE_NAME)
data = pd.read_sql(cmd, connection) 
#print(data)

def read_table(cmd):
    global data
    cursor.execute(cmd)
    data = pd.read_sql(cmd, connection) 
    #print(data.head())

# gather all data
cmd = "SELECT * FROM {}".format(TABLE_NAME)
#read_table(cmd)

# gather data from specific dates (or any specified column)
col = "Date"
var = "2021"
cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLE_NAME,col,var)
read_table(cmd)

def plot_allvalues():
    print("Attempt plot")
    ax = plt.gca()
    data.plot(kind='line',x='Date',y='TotalValue',color='g',ax=ax)
    data.plot(kind='line',x='Date',y='InvValue',color='b',ax=ax)
    data.plot(kind='line',x='Date',y='Investment',color='b',linestyle='dashed',ax=ax)
    data.plot(kind='line',x='Date',y='PieValue',color='orange',ax=ax)
    data.plot(kind='line',x='Date',y='PieInvestment',color='orange',linestyle='dashed',ax=ax)
    plt.show()

def plot_invvalue():
    print("Attempt plot for Investment value")
    ax = plt.gca()
    data.plot(kind='line',x='Date',y='InvValue',color='green',ax=ax)
    data.plot(kind='line',x='Date',y='Investment',color='orange',ax=ax)
    plt.show()

def plot_pievalue():
    print("Attempt plot for Pie value")
    ax = plt.gca()
    data.plot(kind='line',x='Date',y='PieValue',color='green',ax=ax)
    data.plot(kind='line',x='Date',y='PieInvestment',color='orange',ax=ax)
    plt.show()

def plot_realised():
    print("Attempt plot")
    ax = plt.gca()
    data.plot(kind='line',x='Date',y='Realised',ax=ax)
    plt.show()

#plot_pievalue()
plot_invvalue()
