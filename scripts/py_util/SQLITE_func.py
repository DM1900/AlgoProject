import sqlite3
from sqlite3.dbapi2 import Cursor

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

def GetSuggestions(VAR):
    # define connection & cursor
    DB_FOLDER = '/home/admin/AlgoProject/scripts/db/' 
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
        if var == "Both":
            var = "IN ('{}','{}')".format("BUY","SELL")
        else:
            var = "LIKE '%{}%'".format(var)
        cmd = "SELECT entry_id,Ticker,Suggestion FROM {} WHERE {} {}".format(TABLE_NAME,COL,var)
        global results
        cursor.execute(cmd)
        results = cursor.fetchall()
        return results

    GetLastTable()
    read_table(VAR)

    return results

#VAR = input("Choose to view BUY or SELL (Leave blank for both): ") or "Both"# ask user to enter year
#VAR = "Both"
#GetSuggestions(VAR)
#print(results)

#def ListResults():
#    for x in results:
#        print("{},{},{},{}".format(x[0],x[2],x[7],x[8]))
#ListResults()
#end