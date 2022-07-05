import serial
from serial.serialutil import SerialException
import os
import time
from datetime import datetime


Time = str(time.strftime('%Y-%m-%d'))
logName = "E:\\DHTlogs\\log"+Time+".csv"
timeSpecific = str(time.strftime('%H:%M:%S')) + ","

class WrongPortException(Exception):
            ''' detects an invalid port  '''
            pass

def log_writer(file_name, input):
        log = open(file_name,'a',newline='')
        log.write(input)
        log.close()

def main():
    print("Started at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    while 1:
        #filepath check 
        if not os.path.exists("E:\\DHTlogs\\"):
                    os.mkdir("E:\\DHTlogs\\")
        # file check
        if not os.path.exists(logName):
                    log = open(logName, 'w+')
                    log.write("Time,Status,Hum,Temp\n")
                    log.close()
        #try to decocde 
        try:        
            data = str(ser.readline().decode('utf-8'))
        except UnicodeDecodeError:
            data = ""
        # writes to .csv
        try:
            timeSpecific = str(time.strftime('%H:%M:%S')) + ","
            log_writer(logName, timeSpecific + data)
        except Exception:
            pass
            

if __name__ == "__main__":
        while True:
                try:
                        print("Enter port: \n>", end="")
                        port = input()
                        ser = serial.Serial(port, 9600, timeout=10)
                        testData = str(ser.readline().decode('utf-8'))
                        if testData == "" or None:
                            raise WrongPortException
                        break
                except SerialException:
                        print("\nInvalid port, try again\n")
                except WrongPortException:
                    print("\nSensor device not found or active, try again\n ")
        if ser.isOpen():
            try:
                main()
            except KeyboardInterrupt:
                print("Ended at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        else:
                print("ERROR: CAN't OPEN CONNECTION")
        ser.close()