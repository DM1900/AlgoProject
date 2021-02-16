#!/usr/bin/python3.9
# DerekM - 2021
# The data is gathered from Alpha Vantage which has a delay of 1 day on all stock data.
# Please factor that into any tradng decisions (this is based on Daily RSI so it's not such a big issue here)
#
# imports:
import logging
from datetime import datetime, timedelta
import pandas as pd
from pandas_datareader import data
from pandas_datareader._utils import RemoteDataError

import sys
import random
import time
import csv
#
#
keys = "scripts/AlphaVantage/keys/keys.txt" # list of alpha vantage keys
#
def GetAPIkey(): # get a new API key each time the script runs
    try:
        #logging.info("Get API Key")
        lines = open(keys).read().splitlines()
        global APIkey
        APIkey = random.choice(lines)
        print(APIkey)
        #logging.info("Got API key, {key}, now waiting to continue...".format(key = APIkey))
    except:
        logging.exception("Error getting API key")
        #time.sleep(WAITERR)

GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()
GetAPIkey()

# end
# end