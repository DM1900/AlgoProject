print("Start")
print("Load packages")
#from alpha_vantage.timeseries import TimeSeries
from alpha_vantage import TimeSeries
print("Get API Key")

#lines = open('keys.txt').read().splitlines()
#APIkey = random.choice(lines)
print(APIkey)
YOUR_API_KEY = "T36W24357QF5Z698"
ts = TimeSeries(key='YOUR_API_KEY')
gq = GLOBAL_QUOTE(key='YOUR_API_KEY')
# Get json object with the intraday data and another with  the call's metadata
#data, meta_data = ts.get_intraday('AAPL')
#print("Print Data")
#print(data.tail(4))

TICKER = ['AAPL']
#TICKER = ['LON:BP.L']
#TICKER = ['BMW.FRK']







print('Ticker: {t}'.format(t=TICKER))

gq = GLOBAL_QUOTE



#ts = TimeSeries(key='YOUR_API_KEY', output_format='pandas')
#data, meta_data = ts.get_intraday(symbol=TICKER)
#TEST = ts.global(symbol=TICKER)
#print(data.head(2))



#https://www.alphavantage.co/query?function=TimeSeries&symbol=LON:BP.L&apikey=T36W24357QF5Z698
#https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=LON:BP.L&apikey=T36W24357QF5Z698