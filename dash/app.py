# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_html_components as html
import pandas as pd

# imports:
from datetime import datetime, timedelta
from pandas_datareader import data
import sqlite3
from sqlite3.dbapi2 import Cursor


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

df = pd.read_sql(cmd, connection)


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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Buy/Sell list'),
    generate_table(df)
])

if __name__ == '__main__':
    app.run_server(debug=True)