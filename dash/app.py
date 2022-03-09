# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# dash modules
import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
# others
from dash.dependencies import Input, Output
import pandas as pd
from datetime import datetime, timedelta
from pandas_datareader import data
import sqlite3
from sqlite3.dbapi2 import Cursor
from dash.dependencies import Input, Output
#import dash_bootstrap_components as dbc+
# Custom functions
from py_util import ViewStats
from py_util import SQLITE_func
from vars import *

# define connection & cursor
RPATH = "/home/derek/AlgoProject"
DB_FOLDER = "{}/scripts/db/".format(RPATH)

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
BUYSELLLIST = TABLE_NAME
"""
TABLES = TABLELIST[0]
TABLESS = "{},{}".format(TABLELIST[0],TABLES[1])
print(TABLES)
exit()
def STOCKGRAPH(var):
    global fig2
    col = "Ticker"
    cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLESS,col,var)
    dfs = pd.read_sql(cmd, connection)
    fig2 = px.line(dfs, x="Date", y="Price")
    return fig2

STOCKGRAPH("AAPL")
"""

COL = "Suggestion"
cmd = "SELECT * FROM {} WHERE {} IN ('BUY','SELL')".format(TABLE_NAME,COL)
df0 = pd.read_sql(cmd, connection)
df0 = df0.drop('Action', axis=1)
df0 = df0.sort_values('RSI')

cmd = "SELECT * FROM {} ".format(TABLE_NAME)
df3 = pd.read_sql(cmd, connection)
df3 = df3.drop('Action', axis=1)
df3 = df3.sort_values('RSI')

# list of tickers
TICKERSLIST = "{}/tickers/AV/tickerfile_TRADELIST.txt".format(RPATH)
df4 = pd.read_csv(TICKERSLIST, delimiter = "\t")

# get last row:
LRESULTS = SQLITE_func.GetLastRow()
#LID = LRESULTS[0]
#LTABLEDATE = LRESULTS[1]
#LTOTAL = LRESULTS[2]
LINV = LRESULTS[3]
LREAL = LRESULTS[4]
LDIV = LRESULTS[5]

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
    df1 = df1.drop('InvValue', axis=1)

Get_Stats_ALL()

def Get_Stats(choice):
    global df2
    STATSVALUE = ViewStats.Get_Stats(choice)
    STATSVALUE = STATSVALUE.split(",")
    to_append = STATSVALUE
    a_series = pd.Series(to_append, index = df2.columns)
    df2 = df2.append(a_series, ignore_index=True)

#Get_Stats(2022)
Get_Stats(2021)
Get_Stats(2020)

df2 = df2.drop('InvValue', axis=1)

### Charts
# Create your connection.
DB_FOLDER = './scripts/db/' 
DB_NAME = 'pnl.db'
DB_NAME = '{}{}'.format(DB_FOLDER,DB_NAME) # this DB stores all account value data
#print(DB_NAME)
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

# gather data from specific dates (or any specified column)
def GRAPHTOTAL(var):
    global fig
    col = "Date"
    cmd = "SELECT * FROM {} WHERE {} LIKE '%{}%'".format(TABLE_NAME,col,var)
    df3 = pd.read_sql(cmd, connection)
    fig = px.line(df3, x="Date", y=['TotalValue','Investment','Realised'])
    #fig.add_scatter(x=df3['Date'], y=df3['Investment'])
    return fig
GRAPHYEAR = 2021
GRAPHTOTAL(GRAPHYEAR)

### 

external_stylesheets = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
#external_stylesheets = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css'
#external_stylesheets = 'https://codepen.io/chriddyp/pen/dZVMbK.css'
#external_stylesheets = 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/darkly/bootstrap.min.css'
#external_stylesheets = 'https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css'

app = dash.Dash(__name__)#,external_stylesheets=[external_stylesheets])

TIME = datetime.now()
FOOTER = "{}".format(TIME)

app.layout = html.Div(children=[
    html.H4(children='Buy/Sell list'), 
    html.H6(children="{} | RSI Low: {}, RSI High {}".format(BUYSELLLIST,RSILOW,RSIHIGH)),
    dash_table.DataTable(
    id='BuySell',
    columns=[{"name": i, "id": i} for i in df0.columns],
    data=df0.to_dict('records'),
    style_table={ 
        'overflowX': 'auto',
        'width': '50%'
        },
    style_as_list_view=True,
    style_header={'backgroundColor': '#1F2739'},
    style_cell={
        'backgroundColor': '#323C50',
        'color': 'white'
        },
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{{Suggestion}} = {}'.format("BUY"),
                'column_id': 'Suggestion'
            },
            'color': 'green'
        },
                {
            'if': {
                'filter_query': '{{Suggestion}} = {}'.format("SELL"),
                'column_id': 'Suggestion'
            },
            'color': 'red'
        },
        {
            'if': {
                'filter_query': '{RSI} > 70',
                'column_id': 'RSI'
            },
            'color': 'red',
        },
        {
            'if': {
                'filter_query': '{RSI} > 70',
                'column_id': 'Ticker'
            },
            'color': 'red'
        },  
        {
            'if': {
                'filter_query': '{RSI} < 35',
                'column_id': 'RSI'
            },
            'color': 'green',
        },
        {
            'if': {
                'filter_query': '{RSI} < 35',
                'column_id': 'Ticker'
            },
            'color': 'green'
        }, 

    ]
    ),
    #
    html.H4(children="All Tickers"),
    dash_table.DataTable(
    id='AllTickers',
    columns=[{"name": i, "id": i} for i in df3.columns],
    data=df3.to_dict('records'),
    page_action='none',
    style_table={
        'height': '150px', 
        'overflowY': 'auto',
        'overflowX': 'auto',
        'width': '50%',
        },
    style_as_list_view=True,
    style_header={'backgroundColor': '#1F2739'},
    style_cell={
        'backgroundColor': '#323C50',
        'color': 'white'
        },
    style_data_conditional=[
        {
            'if': {
                'filter_query': '{{Suggestion}} = {}'.format("BUY"),
                'column_id': 'Suggestion'
            },
            'color': 'green',
            'fontWeight': 'bold'
        },
                {
            'if': {
                'filter_query': '{{Suggestion}} = {}'.format("SELL"),
                'column_id': 'Suggestion'
            },
            'color': 'red'
        },
        {
            'if': {
                'filter_query': '{RSI} > 70',
                'column_id': 'RSI'
            },
            'color': 'red'
        },       
        {
            'if': {
                'filter_query': '{RSI} < 35',
                'column_id': 'RSI'
            },
            'color': 'green'
        },
    ]
    ),
    #html.Hr(), 
    html.H4(children='Yearly Account Data'),
    #generate_table(df2),
    dash_table.DataTable(
    id='AccData',
    columns=[{"name": i, "id": i} for i in df2.columns],
    data=df2.to_dict('records'),
    style_table={
        'overflowX': 'auto',
        'width': '50%',
    },
    style_as_list_view=True,
    style_header={'backgroundColor': '#1F2739'},
    style_cell={
        'backgroundColor': '#323C50',
        'color': 'white'
    },
    ),
    html.H4(children='Account Data (Cumulative)'),
    #generate_table(df1),
    dash_table.DataTable(
    id='AccData_AllTime',
    columns=[{"name": i, "id": i} for i in df1.columns],
    data=df1.to_dict('records'),
    style_table={
        'overflowX': 'auto',
        'width': '50%',
    },
    style_as_list_view=True,
    style_header={'backgroundColor': '#1F2739'},
    style_cell={
        'backgroundColor': '#323C50',
        'color': 'white'
    },
    ),
    #html.Hr(),
    html.H4(children='Enter Data'),
    # input button
    dcc.Input(id="Total", type="number", placeholder="Total account value"),
    dcc.Input(id="Inv", type="number", placeholder="Total invested (€{})".format(LINV)),
    dcc.Input(id="Real", type="number", placeholder="Total realised"),
    dcc.Input(id="Div", type="number", placeholder="Total dividend"),
    html.Div(id="number-out"),
    html.Button('Confirm Input', id='btn1', n_clicks=0),
    html.Div(id='container-button-timestamp'),
    # line graph
    #html.H4(children='Graph for {}'.format(GRAPHYEAR)),
    #dcc.Graph(figure=fig),
    #dcc.Graph(figure=fig2),
    html.H6("Page load time: {}".format(FOOTER)),
])

@app.callback(
    # button
    Output('container-button-timestamp', 'children'),
    Input('btn1', 'n_clicks'),
    Input("Total", "value"),
    Input("Inv", "value"),
    Input("Real", "value"),
    Input("Div", "value"),
)
def update_output(event,Total, Inv, Real, Div):
    if event == 0:
        #return "Not Clicked ({})".format(event)
        return ""
    else:
        x = '{}, {}, {}, {}'.format(Total, Inv, Real, Div)
        SQLITE_func.EnterData(Total,Inv,Real,Div)
        #return "Clicked {} times. {}".format(event, x)
        return ""

if __name__ == '__main__':
    app.run_server(debug=True)
