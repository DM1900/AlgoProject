# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# dash modules
import dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
# others
from dash.dependencies import Input, Output
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

### Charts
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

df2 = pd.read_sql(cmd, connection)

#print(df2)
#exit()
###



#df2 = px.data.gapminder().query("continent=='Oceania'")
fig = px.line(df2, x="Date", y="TotalValue")


###

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.13.0/css/all.min.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']

app = dash.Dash(__name__)#,external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H4(children='Buy/Sell list'),
    generate_table(df0),
    html.Hr(),
    html.H4(children='Yearly Account Data'),
    generate_table(df2),
    html.H4(children='Account Data (Cumulative)'),
    generate_table(df1),
    html.Hr(),
    html.H4(children='Enter Data'),
    # input
    dcc.Input(id="Total", type="number", placeholder="Total account value"),
    dcc.Input(id="Inv", type="number", placeholder="Total invested amount"),
    dcc.Input(id="Real", type="number", placeholder="Total realised amount"),
    dcc.Input(id="Div", type="number", placeholder="Total dividend amount"),
    html.Div(id="number-out"),
    # button
    html.Button('Button 1', id='btn1', n_clicks=0),
    html.Div(id='container-button-timestamp'),
    dcc.Graph(figure=fig),
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
    SUM = event #Total + Inv + Real + Div + event
    return 'This is a test of the button {}, {}, {}, {}, {}, {}'.format(SUM,event,Total, Inv, Real, Div)
    #SQLITE_func.EnterData(Total,Inv,Real,Div)





if __name__ == '__main__':
    app.run_server(debug=True)