#!/usr/bin/python
# imports:
import logging
from datetime import datetime, timedelta
import pandas as pd
import csv
# Logging variables
logfile = datetime.now().strftime("%Y%m%d-%H%M")
logfile = "logs/AV_log_{}.log".format(logfile)
logging.basicConfig(filename=logfile, encoding='utf-8', level=logging.DEBUG)
# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=logfile,
                    filemode='w')
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
# set a format which is simpler for console use
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger().addHandler(console)
#
logging.info(datetime.now())

try:
    CSV_FILE = 'scripts/output/AVData_20210108.csv'
    CSV_FILE = datetime.now().strftime('scripts/output/AVData_%Y%m%d.csv')
    logging.info("Opening CSV file: {}".format(CSV_FILE))

    df2 = pd.read_csv(CSV_FILE)
    df2 = df2[df2.Suggestion != "-"]
    logging.info(df2)
    logging.info("Output 'df2' to CSV file")
    CSV_FILE = datetime.now().strftime('scripts/output/SuggestionDataOnly_%Y%m%d.csv')
    df2.to_csv(CSV_FILE,index=False)
except:
    logging.exception("CSV error")
    #time.sleep(WAITERR)

# end