#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from PyQt5.QtWidgets import QPushButton
from typing import Text

CSS = \
{
    'QWidget':
    {
        'background-color': '#333333',
    },
    'QLabel#label':
    {
        'color': 'white',
        'background-color': '#1d90cd',
        'font-weight': 'bold',
        'padding': '15px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },
    'QLabel#label:active':
    {
        'color': 'white',
        'font': 'georgia',
        'font-weight': 'bold',
        'font-size': '16px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },

    'QPushButton#button':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '25px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },
    'QPushButton#button:active':
    {
        'color': '#ffffff',
    },
    'QPushButton#button:hover':
    {
        'color': '#1d90cd',
    },

    'QPushButton#exitbutton':
    {
        'color': '#888888',
        'background-color': '#444444',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '25px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },
    'QPushButton#exitbutton:active':
    {
        'color': '#ffffff',
    },
    'QPushButton#exitbutton:hover':
    {
        'color': 'red',
    },

    'QLabel#acdata':
    {
        'color': '#ffffff',
        'background-color': '#444444',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '25px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },
}
 
def dictToCSS(dictionnary):
    stylesheet = ""
    for item in dictionnary:
        stylesheet += item + "\n{\n"
        for attribute in dictionnary[item]:
            stylesheet += "  " + attribute + ": " + dictionnary[item][attribute] + ";\n"
        stylesheet += "}\n"
    return stylesheet
 
def create_chart():
    print("Generating chart")
    pycmd = 'python /home/admin/AlgoProject/scripts/41_VisualiseData.py'
    os.system(pycmd)

def show_portfolio():
    print("This is a test!")
    #pycmd = 'pritn("This is a test!")'
    #os.system(pycmd)

def get_stock_data():
    check = input("Are you sure? could take 25 minutes! (y or n) ") or "n"
    if check == "y":
        print("Generating stock suggestion data")
        pycmd = 'python /home/admin/AlgoProject/scripts/02_get_data_sqlite.py'
        os.system(pycmd)
    else:
        print("No action taken")

def enter_data():
    print("Enter data...")
    pycmd = 'python /home/admin/AlgoProject/scripts/32_EnterData_sqlite.py'
    os.system(pycmd)

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
    DPIV = 0 # round((((DPIE / DPIEINV)-1)*100) ,1)

# gather data for specific year
YEAR = 0 # input("Choose year to gather data for (leave blank to gather all data): ") or "0" # ask user to enter year

col = "entry_id"
cmd = 'SELECT * FROM {} ORDER BY {} DESC LIMIT 1'.format(TABLE_NAME,col) # Get all data
read_table(cmd)
DATA = results[0]
#print(DATA)
get_data(DATA)

TEXT1 = """Total value of account is €{}
Realised value is €{}
Diviend recieved is €{}

Stock value is €{}
Stock investment is €{}
Stock value increase is {}%

Pie value is €{}
Pie investment is €{}
Pie value increase is {}%""".format(DTOTAL,DREAL,DDIV,DVAL,DINV,DPER,DPIE,DPIEINV,DPIV)

# start gui 
class Main(QtWidgets.QMainWindow):
    def __init__(self, parent):
        super().__init__()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setStyleSheet(dictToCSS(CSS))
        self.resize(250, 250)
        self.ui = QtWidgets.QWidget(self)
        self.setCentralWidget(self.ui)

        self.ui.label = QtWidgets.QLabel("Account Data")
        self.ui.label.setObjectName("label")
        self.ui.label.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.portfolio = QtWidgets.QPushButton("Portfolio Info")
        self.ui.portfolio.setObjectName("button")
        self.ui.portfolio.clicked.connect(show_portfolio)
        self.ui.portfolio.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.createchart = QtWidgets.QPushButton("Create Chart")
        self.ui.createchart.setObjectName("button")
        self.ui.createchart.clicked.connect(create_chart)
        self.ui.createchart.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.enterdata = QtWidgets.QPushButton("Enter data")
        self.ui.enterdata.setObjectName("button")
        self.ui.enterdata.clicked.connect(enter_data)
        self.ui.enterdata.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.getdata = QtWidgets.QPushButton("Gather Data")
        self.ui.getdata.setObjectName("button")
        self.ui.getdata.clicked.connect(get_stock_data)
        self.ui.getdata.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.exitbutton = QtWidgets.QPushButton("Exit")
        self.ui.exitbutton.setObjectName("exitbutton")
        self.ui.exitbutton.clicked.connect(self.close)
        self.ui.exitbutton.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.acdata1 = QtWidgets.QLabel(TEXT1)
        self.ui.acdata1.setObjectName("acdata")
        self.ui.acdata1.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.layoutmain = QtWidgets.QHBoxLayout() # Horozontal layout that hols the others

        self.ui.layout2 = QtWidgets.QVBoxLayout()
        self.ui.layout2.setContentsMargins(0, 0, 50, 0)
        self.ui.layout2.addWidget(self.ui.label)
        #self.ui.layout2.addWidget(self.ui.portfolio)
        self.ui.layout2.addWidget(self.ui.createchart)
        self.ui.layout2.addWidget(self.ui.enterdata)
        self.ui.layout2.addWidget(self.ui.getdata)
        self.ui.layout2.addWidget(self.ui.exitbutton)
        #self.ui.setLayout(self.ui.layout2)

        self.ui.layout3 = QtWidgets.QVBoxLayout()
        self.ui.layout3.setContentsMargins(0, 0, 50, 0)
        self.ui.layout3.addWidget(self.ui.acdata1)
        #self.ui.setLayout(self.ui.layout3)

        self.ui.layoutmain.addLayout(self.ui.layout2) # vertical layout
        self.ui.layoutmain.addLayout(self.ui.layout3) # vertical layout

        self.ui.setLayout(self.ui.layoutmain)

        self.show()
 
    def mouseMoveEvent(self, event):
        # Enable mouse dragging
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()
 
    def mousePressEvent(self, event):
        # Enable mouse dragging
        if event.button() == QtCore.Qt.LeftButton:
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
 
    def keyPressEvent(self, event):
        # Escape key close the window
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        QtWidgets.QMainWindow.keyPressEvent(self, event)
 
    def paintEvent(self, event):
        # Draw a one pixel border
        borderColor = QtGui.QColor("black")
        bgColor = QtGui.QColor(self.palette().color(QtGui.QPalette.Background))
        painter = QtGui.QPainter(self)
        painter.setPen(QtCore.Qt.NoPen)
        painter.setBrush(QtGui.QBrush(borderColor))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QtGui.QBrush(bgColor))
        painter.drawRect(1, 1, self.width()-2, self.height()-2)
 
 
if __name__== '__main__':
    app = QtWidgets.QApplication([])
    gui = Main(app)
    sys.exit(app.exec_())
