#!/usr/bin/python3.9
print("Start")
print("Load packages")
#import sys
import random
from datetime import datetime, timedelta, date
import time

logfile = datetime.now()
print(logfile)

time.sleep(2)

time2 = datetime.now()
print(time2)

ans = time2 - logfile

print(ans)

f = open("/home/admin/AlgoProject/scripts/AlphaVantage/CronTest01.txt", "w")
f.write("Start {}, Finish {}, Total {}".format(logfile, time2, ans))
f.close()