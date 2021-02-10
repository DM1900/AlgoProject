import pandas as pd
from datetime import datetime, timedelta



YEAR = datetime.now().strftime("%Y")
#YEAR = int(YEAR)
#YEAR = YEAR-1
print(YEAR)
# FILE = "/home/admin/AlgoProject/scripts/AlphaVantage/data/stock_2020.csv"



FILE = "/home/admin/AlgoProject/scripts/AlphaVantage/data/stock_{}.csv".format(YEAR)
print(FILE)

df = pd.read_csv(FILE)
pd.set_option("display.max.columns",None)
print(df.tail())
