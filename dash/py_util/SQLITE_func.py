import sqlite3
from sqlite3.dbapi2 import Cursor
from datetime import datetime, timedelta

DB_FOLDER = '/home/derek/AlgoProject/scripts/db/' 
#DB_FOLDER = './scripts/db/' 


def CreateDB(DB_NAME,TABLE_NAME):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    command1 = """CREATE TABLE IF NOT EXISTS {} (
        entry_id INTEGER PRIMARY KEY,
        Date DATE,
        Ticker TEXT,
        Price DECIMAL(16, 2),
        PreviousClose DECIMAL(16, 2),
        Change TEXT,
        RSI DECIMAL(4, 2),
        Suggestion TEXT,
        Action TEXT
    )""".format(TABLE_NAME)

    cursor.execute(command1)
    connection.commit()

# View Suggestions
def GetLastTable():
    global TABLE_NAME
    cmd = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC LIMIT 1"
    cursor.execute(cmd)
    TABLE = cursor.fetchall()
    x = TABLE[0]
    TABLE_NAME = x[0]
    return x

def read_table(var):
    if var == "Both":
        var = "IN ('{}','{}')".format("BUY","SELL")
    else:
        var = "LIKE '%{}%'".format(var)
    cmd = "SELECT * FROM {} WHERE {} {}".format(TABLE_NAME,COL,var)
    global results
    cursor.execute(cmd)
    results = cursor.fetchall()
    for x in results:
        print("{},{},{},{}".format(x[0],x[2],x[7],x[8]))

def GetLastRow():
    # define connection & cursor
    DB_NAME = 'pnl.db'
    DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # get last row for comparison data
    TABLE_NAME = "pldata"
    cmd = """SELECT * FROM {} ORDER BY entry_id DESC LIMIT 1""".format(TABLE_NAME)
    LASTROW = cursor.execute(cmd).fetchone()
    # variables:
    LID = LASTROW[0]
    LTABLEDATE = LASTROW[1]
    LTotalValue = LASTROW[2]
    LInvestment = LASTROW[4]
    LRealised = LASTROW[6]
    LDividend = LASTROW[7]
    LInvValue = LASTROW[8]

    LResults = [LID,LTABLEDATE,LTotalValue,LInvestment,LRealised,LDividend,LInvValue]
    #print(LResults)
    return LResults

def GetSuggestions(VAR):
    # define connection & cursor
    DB_NAME = 'StockData.db'
    DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # create table:
    COL = "Suggestion"

    def GetLastTable():
        global TABLE_NAME
        cmd = "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name DESC LIMIT 1"
        cursor.execute(cmd)
        TABLE = cursor.fetchall()
        x = TABLE[0]
        TABLE_NAME = x[0]
        return x

    def read_table(var):
        SELECTIONS = "entry_id,Ticker,Price,Change,RSI,Suggestion"
        if var == "Both":
            var = "IN ('{}','{}')".format("BUY","SELL")
        else:
            var = "LIKE '%{}%'".format(var)
        cmd = "SELECT {} FROM {} WHERE {} {}".format(SELECTIONS,TABLE_NAME,COL,var)
        global results
        cursor.execute(cmd)
        results = cursor.fetchall()
        return results

    GetLastTable()
    read_table(VAR)
    return results

def EnterData(TotalValue,Investment,Realised,Dividend):
    # define connection & cursor
    DB_NAME = 'pnl.db'
    DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    # entry_id,Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend
    TABLE_NAME = "pldata"
    VALUE = TotalValue
    DATE = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 
    #DATE = """{}""".format(DATE)
    INSERT_CMD = 'INSERT INTO {} VALUES (NULL,"{}",{},{},{},{},{},{},{})'.format(TABLE_NAME,DATE,TotalValue,0,Investment,0,Realised,Dividend,VALUE)
    print(INSERT_CMD)
    cursor.execute(INSERT_CMD)
    connection.commit()

#EnterData(2190.76,1800,521.69,9.49)    

def DeleteRow(COL,VAL):
    DB_NAME = 'pnl.db'
    DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    TABLE_NAME = "pldata"

    cmd = "DELETE FROM {} WHERE {} = {}".format(TABLE_NAME,COL,VAL)
    cursor.execute(cmd)
    connection.commit()

