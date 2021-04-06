import sys
import os
from datetime import datetime, timedelta
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pandas as pd
# Custom functions
from py_util import ViewStats
from py_util import SQLITE_func
#
from qt_material import apply_stylesheet

class RuntimeStylesheets(QMainWindow):
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('main_window.ui', self)
        self.main.pushButton_2.setProperty('class', 'big_button')

# stats:
def Get_Stats(choice):
    global STATS
    STATSVALUE = ViewStats.Get_Stats(choice)
    #print(STATSVALUE)
    STATS = """{}""".format(STATSVALUE)

class StatsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        Get_Stats(CHOICE) # returns a variable STATS

        self.setWindowTitle("STATS!")

        QBtn = QDialogButtonBox.Ok #| QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel(STATS)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

# suggestions:
class pandasModel(QAbstractTableModel):
    def __init__(self, data):
        QAbstractTableModel.__init__(self)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parnet=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class ChoiceDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(650, 520)

        SUGG = SQLITE_func.GetSuggestions(CHOICE)
        df = pd.DataFrame(SUGG)
        self.setWindowTitle("Trading Suggestions!")

        QBtn = QDialogButtonBox.Ok #| QDialogButtonBox.Cancel

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        
        message1 = QLabel("{}".format(CHOICE))

        model = pandasModel(df)
        view = QTableView()
        view.setModel(model)

        self.layout.addWidget(message1)
        self.layout.addWidget(view)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class EnterDataDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Enter Data!")

        LRESULTS = SQLITE_func.GetLastRow()
        print(LRESULTS)
        #LID = LRESULTS[0]
        #LTABLEDATE = LRESULTS[1]
        #LTOTAL = LRESULTS[2]
        LINV = LRESULTS[3]
        LREAL = LRESULTS[4]
        LDIV = LRESULTS[5]
        #LINVV = LRESULTS[6]

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        #self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("Enter data about the account")
        statsfont = message.font()
        statsfont.setPointSize(20)
        message.setFont(statsfont)
        message.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


        box0 = QLabel("'entry_id' and 'Date' added automatically")
        box0font = box0.font()
        box0font.setPointSize(12)
        box0.setFont(box0font)
        box0.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        
        #ENTRY_ID = "NULL"
        #DATE = datetime.now().strftime("%d/%m/%Y") # "%Y%m%d-%H%M") # input("Enter the date (dd/mm/yyyy): ") 

        box1 = QLineEdit()
        box1.setMaxLength(10)
        box1.setPlaceholderText("Total account value: ")
        box1.returnPressed.connect(self.return_pressed)
        box1.selectionChanged.connect(self.selection_changed)
        #box1.textChanged.connect(self.text_changed)
        #box1.textEdited.connect(self.text_edited)
        box1.textEdited.connect(self.text_set_box1)

        box2 = QLineEdit()
        box2.setMaxLength(10)
        box2.setPlaceholderText(f"Total invested amount: (€{LINV})")
        box2.returnPressed.connect(self.return_pressed)
        box2.selectionChanged.connect(self.selection_changed)
        #box2.textChanged.connect(self.text_changed)
        #box2.textEdited.connect(self.text_edited)
        box2.textEdited.connect(self.text_set_box2)

        box3 = QLineEdit()
        box3.setMaxLength(10)
        box3.setPlaceholderText(f"Total realised amount: (€{LREAL})")
        box3.returnPressed.connect(self.return_pressed)
        box3.selectionChanged.connect(self.selection_changed)
        #box3.textChanged.connect(self.text_changed)
        #box3.textEdited.connect(self.text_edited)
        box3.textEdited.connect(self.text_set_box3)

        box4 = QLineEdit()
        box4.setMaxLength(10)
        box4.setPlaceholderText(f"Total dividend amount: (€{LDIV})")
        box4.returnPressed.connect(self.return_pressed)
        box4.selectionChanged.connect(self.selection_changed)
        #box4.textChanged.connect(self.text_changed)
        #box4.textEdited.connect(self.text_edited)
        box4.textEdited.connect(self.text_set_box4)

        process = QPushButton("Process data entry")
        process.clicked.connect(self.process_data_entry)
        process.clicked.connect(self.accept)

        self.layout.addWidget(message)
        self.layout.addWidget(box0) 
        self.layout.addWidget(box1) #BTOTAL
        self.layout.addWidget(box2) #BINV
        self.layout.addWidget(box3) #BREAL
        self.layout.addWidget(box4) #BDIV
        self.layout.addWidget(process)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

    def return_pressed(self):
        print("Return pressed!")
        #self.centralWidget().setText("BOOM!")

    def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())

    def text_changed(self, s):
        print("Text changed...")
        print(s)

    def text_edited(self, s):
        print("Text edited...")
        print(s)

    def text_set_box1(self, t):
        global BTOTAL
        #print("Text edited...")
        BTOTAL = t
        print(BTOTAL)

    def text_set_box2(self, i):
        global BINV
        BINV = i
        print(BINV)

    def text_set_box3(self,r):
        global BREAL
        #print("Text edited...")
        BREAL = r
        print(BREAL)

    def text_set_box4(self, d):
        global BDIV
        #print("Text edited...")
        BDIV = d
        print(BDIV)

    def process_data_entry(a,b):
        print(f"a: {a}")
        print(f"b: {b}")
        #print("Values: {}, {}, {}, {}".format(BTOTAL,BINV,BREAL,BDIV))
        SQLITE_func.EnterData(BTOTAL,BINV,BREAL,BDIV)
        print(SQLITE_func.GetLastRow())

def enter_data():
    print("Enter data...")
    pycmd = 'python ./scripts/32_EnterData_sqlite.py'
    os.system(pycmd)

def create_chart():
    print("Generating chart")
    pycmd = 'python ./scripts/41_VisualiseData.py'
    os.system(pycmd)

def get_stock_data():
    print("Generating stock suggestion data")
    pycmd = 'python ./scripts/02_get_data_sqlite.py'
    os.system(pycmd)

class GetDataDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle("Gather Suggestion data?")

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel

        message = QLabel("Are you sure? May take up to 30 minutes to complete")

        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(get_stock_data)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Trading Account App")

        mainlabel = QLabel("Account Data")
        font = mainlabel.font()
        font.setPointSize(20)
        mainlabel.setFont(font)
        mainlabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        enterdata = QPushButton("Enter Data")
        enterdata.clicked.connect(self.button_clicked_enterdata)

        createchart = QPushButton("Create Chart")
        createchart.clicked.connect(create_chart)

        exitbutton = QPushButton("Exit")
        exitbutton.setObjectName("exitbutton")
        exitbutton.clicked.connect(self.close)
            
        layout = QVBoxLayout() 

        # Layout 2
        layout2 = QHBoxLayout()

        statslabel = QLabel("Stats:")
        statsfont = statslabel.font()
        statsfont.setPointSize(15)
        statslabel.setFont(statsfont)
        statslabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        allstats = QPushButton("All Stats")
        allstats.clicked.connect(self.button_clicked_all)
        ttstats = QPushButton("2020")
        ttstats.clicked.connect(self.button_clicked_2020)
        ttostats = QPushButton("2021")
        ttostats.clicked.connect(self.button_clicked_2021)

        layout2.addWidget(statslabel)
        layout2.addWidget(allstats)
        layout2.addWidget(ttstats)
        layout2.addWidget(ttostats)

        # Layout 3
        # Trade suggestions
        #buttonBox = QDialogButtonBox(QBtn)
        #self.buttonBox.accepted.connect(self.accept)
        #self.buttonBox.rejected.connect(self.reject)

        layout3 = QHBoxLayout()
        
        #message = QLabel(SUGG)
        tradelabel = QLabel("Trade:")
        statsfont = tradelabel.font()
        statsfont.setPointSize(15)
        tradelabel.setFont(statsfont)
        tradelabel.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        buy = QPushButton("Buy")
        buy.clicked.connect(self.button_clicked_buy)

        sell = QPushButton("Sell")
        sell.clicked.connect(self.button_clicked_sell)

        both = QPushButton("Both")
        both.clicked.connect(self.button_clicked_both)

        getdata = QPushButton("Gather Data")
        getdata.clicked.connect(self.button_clicked_getdata)

        layout3.addWidget(tradelabel)
        layout3.addWidget(buy)
        layout3.addWidget(sell)
        layout3.addWidget(both)


        layout.addWidget(mainlabel)
        #layout.addWidget(showdata)
        layout.addLayout(layout2)
        #layout.addWidget(showsugg)
        layout.addLayout(layout3)
        layout.addWidget(enterdata)
        layout.addWidget(createchart)
        layout.addWidget(getdata)
        layout.addWidget(exitbutton)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def button_clicked_buy(self, s):
        global CHOICE
        print("click", s)
        CHOICE = "BUY"
        dlg = ChoiceDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("buySuccess!")
        else:
            print("Cancel!")

    def button_clicked_sell(self, s):
        global CHOICE
        print("click", s)
        CHOICE = "SELL"
        dlg = ChoiceDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("sellSuccess!")
        else:
            print("Cancel!")

    def button_clicked_both(self, s):
        global CHOICE
        print("click", s)
        CHOICE = "Both"
        dlg = ChoiceDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("bothSuccess!")
        else:
            print("Cancel!")

    def button_clicked(self, s):
        print("click", s)

        dlg = StatsDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")

    def button_clicked_all(self, s):
        global CHOICE
        CHOICE = 0
        print("click", s, CHOICE)
        dlg = StatsDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success! {}".format(CHOICE))
        else:
            print("Cancel!")

    def button_clicked_2020(self, s):
        global CHOICE
        CHOICE = 2020
        print("click", s, CHOICE)
        dlg = StatsDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success! {}".format(CHOICE))
        else:
            print("Cancel!")

    def button_clicked_2021(self, s):
        global CHOICE
        CHOICE = 2021
        print("click", s, CHOICE)
        dlg = StatsDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success! {}".format(CHOICE))
        else:
            print("Cancel!")

    def button_clicked_sugg(self, s):
        print("click", s)

        dlg = SuggDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")

    def button_clicked_enterdata(self, s):
        print("click", s)

        dlg = EnterDataDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Data Entered Successfully!")
        else:
            print("Data Entry Cancelled!")

    def button_clicked_getdata(self, s):
        print("click", s)

        dlg = GetDataDialog()  # If you pass self, the dialog will be centered over the main window as before.
        if dlg.exec_():
            print("Success!")
        else:
            print("Cancel!")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()

    # setup stylesheet
    #['dark_amber.xml', 'dark_blue.xml', 'dark_cyan.xml', 'dark_lightgreen.xml', 'dark_pink.xml', 'dark_purple.xml', 'dark_red.xml', 'dark_teal.xml', 'dark_yellow.xml', 
    # 'light_amber.xml', 'light_blue.xml', 'light_cyan.xml', 'light_cyan_500.xml', 'light_lightgreen.xml', 'light_pink.xml', 'light_purple.xml', 'light_red.xml', 'light_teal.xml', 'light_yellow.xml']
    apply_stylesheet(app, theme='light_blue.xml')
    stylesheet = app.styleSheet()
    # app.setStyleSheet(stylesheet + "QPushButton{color: red; text-transform: none;}")
    with open('./scripts/custom.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    window.show()
    app.exec_()
