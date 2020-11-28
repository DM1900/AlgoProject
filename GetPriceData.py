#!/usr/bin/python

#https://www.youtube.com/watch?v=DOHg16zcUCc

#Dependencies:
#Start Python 
#pip install pandas-datareader
#pip install matplotlib
#pip install pandas
#pip install numpy
#pip install datetime

# imports:
print("Load imports")
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import matplotlib.pyplot as pyplt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import csv

#
print("Load variables")
PriceHistory = 28 # no. of days data to gather
START_DATE = str((datetime.today()- timedelta(days=PriceHistory)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
tickerlist = "tickers/tickerfile.txt"
#tickerlist = "tickers/tickerfile_TEST.txt"
with open(tickerlist) as file:
    tickers = [ticker.rstrip('\n') for ticker in file]
#tickers = ['AAPL','AMZN','BP.L']
#tickers = ['MKS.L']

def clean_data(stock_data,col1):
    weekdays = pd.date_range(start=START_DATE, end=END_DATE)
    clean_data = stock_data[col1].reindex(weekdays)
    return clean_data.fillna(method='ffill')

stock_data = data.DataReader(tickers,'yahoo',START_DATE,END_DATE)
stock_data = clean_data(stock_data,'Adj Close')
print(stock_data.tail(14))

def write_csv():
    CSV_FILE = datetime.now().strftime('output/PriceData_%Y%m%d.csv')
    stock_data.tail(24).to_csv(CSV_FILE,index=False)

write_csv()

#data = pd.read_csv(CSV_FILE)
#print(data)
