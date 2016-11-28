"""Setup logging."""
import os
import time
import logging

# ################### Setup logging ########################
LOG_PATH = "./logs"

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOG_FILE = time.strftime("%Y%m%d-%H%M%S")
# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# create file handler
fh = logging.FileHandler("{0}/{1}.log".format(LOG_PATH, LOG_FILE))
fh.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to console handler
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
# ##########################################################
