#!/usr/bin/python
#https://www.youtube.com/watch?v=DOHg16zcUCc

# imports:
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import pandas as pd


###
PriceHistory = 180 # no. of days data to gather
RSI_PERIOD = 14 # no. of days to calculate RSI
###

tickers = ['AAPL']#,'AMZN','BP.L','V','VHYL.L','BRKB','UKDV.L']
# create empty dataframe
df2 = pd.DataFrame(columns=[])#'Adj Close', 'Date', 'Ticker','RSI'


def get_data(ticker):
    try:
        print(ticker)
        stock_data = data.DataReader(ticker,'yahoo')
        print(stock_data.tail(1))

        OPEN = stock_data.Open.tail(1)
        print(OPEN)

    except RemoteDataError:
        print('No data found for {t}'.format(t=ticker))

for ticker in tickers:
    get_data(ticker)

#df2 = df2.sort_values(by=['RSI'], na_position='last')

#print(df2)

#CSV_FILE = datetime.now().strftime('output/RSIData_%Y%m%d.csv')
#df2.to_csv(CSV_FILE,index=False)

#print(datetime.now())

#end