#!/usr/bin/python

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
print("Load imports")
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import matplotlib.pyplot as pyplt
import pandas as pd
import numpy as np

from datetime import datetime, timedelta
import csv

CSV_FILE = datetime.now().strftime('output/PriceData_%Y%m%d.csv')
print(CSV_FILE)

stock_data = pd.read_csv(CSV_FILE)
#print(stock_data.head())
print(stock_data.describe())
print(pd.value_counts(stock_data['AAPL']).plot.bar())
