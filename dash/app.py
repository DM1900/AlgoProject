# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
import pandas as pd
from datetime import datetime, timedelta
from pandas_datareader import data
import sqlite3
from sqlite3.dbapi2 import Cursor
# Custom functions
from py_util import ViewStats
from py_util import SQLITE_func

# define connection & cursor
DB_FOLDER = './scripts/db/' 
#DB_NAME = 'pnl.db'
DB_NAME = 'StockData.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
connection = sqlite3.connect(DB_NAME)
cursor = connection.cursor()
# select table
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
TABLELIST = cursor.fetchall()
TABLE_NAME = TABLELIST[-1]
TABLE_NAME = TABLE_NAME[0]

#df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/c78bf172206ce24f77d6363a2d754b59/raw/c353e8ef842413cae56ae3920b8fd78468aa4cb2/usa-agricultural-exports-2011.csv')
COL = "Suggestion"
cmd = "SELECT * FROM {} WHERE {} IN ('BUY','SELL')".format(TABLE_NAME,COL)

df0 = pd.read_sql(cmd, connection)


# stats:

column_names = ["Date", "TotalValue","Investment","Realised","Dividend","InvValue","Percent"]
#Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend,InvValue
df1 = pd.DataFrame(columns = column_names)
df2 = pd.DataFrame(columns = column_names)

def Get_Stats_ALL():
    global df1
    STATSVALUE = ViewStats.Get_Stats(0)
    STATSVALUE = STATSVALUE.split(",")
    to_append = STATSVALUE
    a_series = pd.Series(to_append, index = df1.columns)
    df1 = df1.append(a_series, ignore_index=True)

Get_Stats_ALL()

def Get_Stats(choice):
    global df2
    STATSVALUE = ViewStats.Get_Stats(choice)
    STATSVALUE = STATSVALUE.split(",")
    to_append = STATSVALUE
    a_series = pd.Series(to_append, index = df2.columns)
    df2 = df2.append(a_series, ignore_index=True)

Get_Stats(2021)
Get_Stats(2020)

#print(df2)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Buy/Sell list'),
    generate_table(df0),
    html.H6(children='---'),
    html.H4(children='Yearly Account Data'),
    generate_table(df2),
    html.H4(children='Account Data (Cumulative)'),
    generate_table(df1)
])

if __name__ == '__main__':
    app.run_server(debug=True)