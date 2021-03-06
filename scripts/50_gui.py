#!/usr/bin/python3
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import os
import sqlite3
from sqlite3.dbapi2 import Cursor
from PyQt5.QtWidgets import QPushButton
from typing import Text
# Custom functions
from py_util import ViewStats

CSS = \
{
    'QWidget':
    {
        #'background-color': '#333333',
        'background-color': '#34495e',
    },
    'QLabel#label':
    {
        'color': 'white',
        #'background-color': '#2980b9',
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
        'color': '#ecf0f1',
        'background-color': '#95a5a6',
        'font-weight': 'bold',
        'border': 'none',
        'padding': '25px',
        'font-family': 'Arial, Helvetica, sans-serif',
    },
    'QPushButton#button:active':
    {
        'color': 'white',
    },
    'QPushButton#button:hover':
    {
        'color': '#34495e',
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
        'color': 'white',
        'background-color': '#e74c3c',
    },

    'QLabel#acdata':
    {
        'color': '#444444',
        'background-color': '#ffffff',
        #'font-weight': 'bold',
        'border': 'none',
        'padding': '25px',
        'font-family': 'Arial, Helvetica, sans-serif',
        'text-align': 'left',
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

#def acdata1(YEAR):
#    global STATS
#    STATS = ViewStats.Get_Stats(YEAR)
# get stat data
def Get_Stats():
    global STATS
    STATS_ALL = ViewStats.Get_Stats(0)  
    STATS_2020 = ViewStats.Get_Stats(2020)  
    STATS_2021 = ViewStats.Get_Stats(2021)
    STATS = """{}
    ---
    {}
    ------
    {}""".format(STATS_2021,STATS_2020,STATS_ALL)

Get_Stats()

# Date,TotalValue,PieValue,Investment,PieInvestment,Realised,Dividend

# pop up dialog
def msgButtonClick(i):
   print("Button clicked is:",i.text())

def showDialog():
   msgBox = QtWidgets.QMessageBox()
   msgBox.setIcon(QtWidgets.QMessageBox.Warning)
   msgBox.setText("""Click ok to continue...""")
   msgBox.setWindowTitle("Create chart?")
   msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
   msgBox.buttonClicked.connect(msgButtonClick)

   returnValue = msgBox.exec()
   if returnValue == QtWidgets.QMessageBox.Ok:
      print('OK clicked')
      create_chart()

def getDataConfirm():
   msgBox = QtWidgets.QMessageBox()
   msgBox.setIcon(QtWidgets.QMessageBox.Warning)
   msgBox.setText("""Click ok to continue...""")
   msgBox.setWindowTitle("Run get data script?")
   msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
   msgBox.buttonClicked.connect(msgButtonClick)

   returnValue = msgBox.exec()
   if returnValue == QtWidgets.QMessageBox.Ok:
      print('OK clicked')
      create_chart()

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

        #self.ui.getstats = QtWidgets.QPushButton("Get Stats")
        #self.ui.getstats.setObjectName("button")
        #self.ui.getstats.clicked.connect(get_stats) #(showDialog)
        #self.ui.getstats.setFocusPolicy(QtCore.Qt.NoFocus)

        self.ui.createchart = QtWidgets.QPushButton("Create Chart")
        self.ui.createchart.setObjectName("button")
        self.ui.createchart.clicked.connect(create_chart) #(showDialog)
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

        self.ui.acdata1 = QtWidgets.QLabel(STATS)
        self.ui.acdata1.setObjectName("acdata")
        self.ui.acdata1.setAlignment(QtCore.Qt.AlignCenter)

        self.ui.layoutmain = QtWidgets.QHBoxLayout() # Horozontal layout that holds the others

        # Layout 2
        self.ui.layout2 = QtWidgets.QVBoxLayout()
        self.ui.layout2.setContentsMargins(0, 0, 50, 0)
        self.ui.layout2.addWidget(self.ui.label)
        #self.ui.layout2.addWidget(self.ui.getstats)
        self.ui.layout2.addWidget(self.ui.createchart)
        self.ui.layout2.addWidget(self.ui.enterdata)
        self.ui.layout2.addWidget(self.ui.getdata)
        self.ui.layout2.addWidget(self.ui.exitbutton)
        #self.ui.setLayout(self.ui.layout2)

        # Layout 3
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
