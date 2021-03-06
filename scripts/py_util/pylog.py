#!/usr/bin/python3.9
# DerekM - 2021
# Logging

from datetime import datetime, timedelta

# Logging variables
#LOGTIME = datetime.now().strftime("%Y%m%d-%H%M")
#LOGTIME = datetime.now().strftime("%Y%m%d-%H")
#LOGFILE = "/home/admin/AlgoProject/logs/"
#LOGFILE = LOGFILE + "Log_{}.log".format(LOGTIME)

LOGTIME = datetime.now().strftime("%Y%m%d-%H%M%S")

def WriteToLog(logfile,msg):
    msg = "{} {}".format(LOGTIME,msg)
    f = open(logfile, "a")
    f.write("""{}
""".format(msg))
    f.close()

#WriteToLog(LOGFILE,"Test message!")