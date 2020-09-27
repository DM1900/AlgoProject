#!/usr/bin/python
# test
#https://www.youtube.com/watch?v=DOHg16zcUCc

"""
#Dependencies:
#Start Python 
pip install pandas-datareader
pip install matplotlib
pip install pandas
pip install numpy
pip install datetime
"""


# imports:
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
#
print("Finished Imports")
print("Define Variables")
#START_DATE = '2020-01-01'
START_DATE = str((datetime.today()- timedelta(days=90)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
print(START_DATE, END_DATE)
#UK_STOCK = 'BP'
#USA_STOCK = 'AMZN'
#USA_STOCK = 'AAPL'
tickers = ['AAPL','BP']
#print(UK_STOCK, USA_STOCK)
print(tickers)

def clean_data(stock_data, col):
	

def get_data(ticker):
	print(ticker)
	try:
		stock_data = data.DataReader(ticker,
									'yahoo',
									START_DATE,
									END_DATE)
		print(stock_data)
	except RemoteDataError:
		print('No data found for {t}'.format(t=ticker))
print("get_data has been set, running it now")

for ticker in tickers:
	get_data(ticker)



#end