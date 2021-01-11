#!/usr/bin/python
import logging
from datetime import datetime

filename1 = datetime.now().strftime("%Y%m%d-%H%M%S")
logfile = "logs/AV_log_{}.log".format(filename1)
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



# things to log
logging.info("test {}".format("Info"))
logging.debug("test {}".format("Debug"))
logging.warning("test {}".format("Warning"))
logging.error("test {}".format("Error"))
logging.critical("test {}".format("Critical"))
