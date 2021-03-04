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
