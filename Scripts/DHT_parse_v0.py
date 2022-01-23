import serial
from serial.serialutil import SerialException
import os
import time
from datetime import datetime


Time = str(time.strftime('%Y-%m-%d'))
logName = "C:\\xtagLogs\\xtag_id_log_"+Time+".csv"


def main():
    if not os.path.exists("C:\\xtagLogs\\"):
                os.mkdir("C:\\xtagLogs\\")
    if not os.path.exists(logName):
                log = open(logName, 'w+')
                log.write("Status,Hum,Temp\n")
                log.close()
