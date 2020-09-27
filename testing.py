#testing


#!/usr/bin/python

# imports:
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError
import matplotlib as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
#
START_DATE = str((datetime.today()- timedelta(days=90)).strftime('%Y-%m-%d'))
END_DATE = str(datetime.now().strftime('%Y-%m-%d'))
UK_STOCK = 'BP'
USA_STOCK = 'AAPL'
print(UK_STOCK)