#!/usr/bin/python
# DerekM - 2021
# The data is gathered from Alpha Vantage which has a delay of 1 day on all stock data.
# Please factor that into any tradng decisions (this is based on Daily RSI so it's not such a big issue here)
#

# imports:
from datetime import datetime, timedelta

# relative path, it's up to you which one to use:
RPATH = "."
RPATH = "/home/admin/AlgoProject"

# Log variables:
LOGTIME = datetime.now().strftime("%Y%m%d-%H")
LOGFILE = "{}/logs/".format(RPATH)
LOGFILE = LOGFILE + "Log_{}.log".format(LOGTIME)

START = datetime.now()
SCRIPTNAME = "'02_get_data_sqlite.py'"

def LogTest(logfile,msg):
    msg = "{} {}".format(LOGTIME,msg)
    f = open(logfile, "a")
    f.write("""{}
""".format(msg))
    f.close()
TESTLOG = "{}/logs/CronRun01.log".format(RPATH)
print(TESTLOG)
LogTest(TESTLOG,"Run confirmation from python script (test)")

exit()
