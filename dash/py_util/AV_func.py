#!/usr/bin/python3.9
# DerekM - 2021
# Alpha Vantage functions

from datetime import datetime, timedelta
#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.techindicators import TechIndicators 
#import sys
import random
#import time
#import csv
#import sqlite3
#from sqlite3.dbapi2 import Cursor

def GetAPIkey(keys): # get a new API key each time the script runs
    try:
        #print("Attempt to get API Key")
        #print(keys)
        lines = open(keys).read().splitlines()
        #global APIkey
        APIkey = random.choice(lines)
        #print("Got API key, {}".format(APIkey))
        return APIkey
    except:
        print("Error getting API key")

def GetSuggestion(RS,DCLOSE,DPRICE,BUY,SELL,HOLD,RSIHIGH,RSIVHIGH,RSILOW,RSIVLOW): # get trading suggestion
    if  RS > RSIVHIGH: 
        SUGGESTION = SELL
    elif RS < RSIVLOW:
        SUGGESTION = BUY
    elif  RS > RSIHIGH: 
        if DCLOSE > DPRICE:
            SUGGESTION = SELL
        else:
            SUGGESTION = HOLD
    elif RS < RSILOW:
        if DCLOSE < DPRICE:
            SUGGESTION = BUY
        else:
            SUGGESTION = HOLD
    else:
        SUGGESTION = HOLD
    
    return SUGGESTION

