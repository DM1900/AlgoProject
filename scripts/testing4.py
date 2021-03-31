

def LogTest(logfile,msg):
    #msg = "{} {}".format(msg)
    f = open(logfile, "a")
    f.write("""{}
""".format(msg))
    f.close()


TEESTL = "/home/admin/AlgoProject/logs/CronRun01.log"
LogTest(TEESTL,"This is a test! ")

