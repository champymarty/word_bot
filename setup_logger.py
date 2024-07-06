import logging
import os
import sys

from constant import DATA_PATH

LOGGER_NAME = "bot_logger"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)
fileDir = os.path.join(DATA_PATH, "logs")
if not os.path.isdir(fileDir):
    os.mkdir(fileDir)

FORMATTER = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s')

file = os.path.join(fileDir, "command.log")
handler = logging.FileHandler(filename=file, encoding="utf-8", mode="w")
handler.setFormatter(FORMATTER)
logger.addHandler(handler)

sysout_handler = logging.StreamHandler(sys.stdout)
sysout_handler.setFormatter(FORMATTER)
logger.addHandler(sysout_handler)

def get_logger():
    return logging.getLogger(LOGGER_NAME)