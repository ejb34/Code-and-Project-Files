#This is manual injection of the XTRA data by downloading it form the internet to the Pi
#and then applying it to the module.

import csv
import serial
import time
from datetime import datetime
import logging
import os
import sys

from serial.serialutil import SerialException
# #GPS+GLONASS Data
# url = 'http://iot1.xtracloud.net/xtra3gr.bin'


#def User_inputs():
        

# def SetupLogging():
#     print("Set up logging")
#     logger.setLevel(logging.DEBUG)
#     logFormat = logging.Formatter(fmt='%(asctime)s, %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
#     fHandler = logging.FileHandler(mainLogPath,mode='w')
#     fHandler.setFormatter(logFormat)
#     logger.addHandler(fHandler)

#     consoleHandler = logging.StreamHandler()
#     consoleHandler.setFormatter(logFormat)
#     logger.addHandler(consoleHandler)
Time = str(time.strftime('%Y/%m/%d'))
logName = "xtag_id_log_" + "" + ".csv"

class DupeError(Exception):
        pass

bt_String = "BTMAC:"
tGUID_String = "TagGUID:"
aGUID_String = "AnimalGUID:"
imei_String = "IMEI:"
iccid_String = "ICCID:"
v_String = "SDCVoltageGood:"
cellfw_string = "CellFWVersion:"
sw_string = "SWVersion:"
hash_string = "Hash:"
gyro_pass_string = "Accel/gyro self test passed"
comp_pass_string = "Compass self test passed"
baro_pass_string = "Barometer self test passed"

identifiers = ["SN","Tag GUID","IMEI","ICCID","MAC Address","Animal GUID",
        "SDC Voltage","VBAT & VSOLAR","Cell FW Version","SW Version","Hash", "Accel/gyro self test",
        "Compass self test","Barometer self test"] 


def log_writer(file_name, input):
        log = open(file_name,'a',newline='')
        # writer = csv.writer(f)
        # writer.writerow(input)
        log.write(input)
        log.close()

def ser_listen_and_log(sn):
        # i = []
        d = [None] * 13
        strings = [None] * 13
        strings[0] = sn
        line = ""
        for x in range(0, 200):        
                output = str(ser.readline().decode('utf-8'))
                #tag guid
                if output.find("Tag GUID") != -1 and d[identifiers.index("Tag GUID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(tGUID_String,"")
                        output = output.replace("\n","")
                        if output not in strings:
                                d[identifiers.index("Tag GUID")] = True
                                # i.append(output)
                                print("Tag GUID obtained...")
                                strings[identifiers.index("Tag GUID")] = output
                #animal guid
                if output.find("Animal GUID") != -1 and d[identifiers.index("Animal GUID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(aGUID_String,"")
                        output = output.replace("\n","")
                        if output not in strings:
                                d[identifiers.index("Animal GUID")] = True
                                # i.append(output)
                                print("Animal GUID obtained...")
                                strings[identifiers.index("Animal GUID")] = output
                #IMEI
                if output.find("IMEI") != -1 and d[identifiers.index("IMEI")] == None:
                        output = output.replace(" ","")
                        output = output.replace(imei_String,"")
                        output = output = output.replace("\n","")
                        if output not in strings:        
                                d[identifiers.index("IMEI")] = True
                                # i.append(output)
                                print("IMEI obtained...")
                                strings[identifiers.index("IMEI")] = output
                #ICCID
                if output.find("ICCID") != -1 and d[identifiers.index("ICCID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(iccid_String,"")
                        output = output = output.replace("\n","")
                        if output not in strings:        
                                d[identifiers.index("ICCID")] = True
                                # i.append(output)
                                print("ICCID obtained...")
                                strings[identifiers.index("ICCID")] = output
                #mac address
                if output.find("MAC") != -1 and d[identifiers.index("MAC Address")] == None:
                        output = output.replace(" ","")
                        output = output.replace(bt_String,"")
                        output = output = output.replace("\n","")
                        if output not in strings:
                                d[identifiers.index("MAC Address")] = True
                                # i.append(output)
                                print("MAC address obtained...")
                                strings[identifiers.index("MAC Address")] = output
                #SDC voltage
                if output.find("SDC Voltage Good:") != -1 and d[identifiers.index("SDC Voltage")] == None:
                        output = output.replace(" ","")
                        output = output.replace(v_String,"")
                        output = output.replace("\n","")
                        if output not in strings:
                                d[identifiers.index("SDC Voltage")] = True
                                # i.append(output)
                                print("SDC Voltage obtained...")
                                strings[identifiers.index("SDC Voltage")] = output

                #additions
                #VBAT VSOLAR
                if output.find("VBAT") != -1 and d[identifiers.index("VBAT & VSOLAR")] == None:
                        output = output.replace(" ","")
                        output = output.replace("\n","")
                        if output not in strings:
                                d[identifiers.index("VBAT & VSOLAR")] = True
                                # i.append(output)
                                print("VBAT & VSOLAR obtained...")
                                strings[identifiers.index("VBAT & VSOLAR")] = output
                #cell fw
                if output.find("Cell FW Version") != -1 and d[identifiers.index("Cell FW Version")] == None:
                        output = output.replace(" ","")
                        output = output.replace(cellfw_string,"")
                        output = output = output.replace("\n","")
                        if output not in strings:        
                                d[identifiers.index("Cell FW Version")] = True
                                # i.append(output)
                                print("Cell FW Version obtained...")
                                strings[identifiers.index("Cell FW Version")] = output
                #sw version and hash
                if output.find("SW Version") != -1 and d[identifiers.index("SW Version")] == None:
                        output = output.replace(" ","")
                        output = output.replace(sw_string,"")
                        output = output.replace(hash_string,"")
                        output = output = output.replace("\n","")
                        if output not in strings:        
                                d[identifiers.index("SW Version")] = True
                                # i.append(output)
                                print("SW Version obtained...")
                                strings[identifiers.index("SW Version")] = output
                #gyro test
                if output.find("Accel/gyro self test") != -1 and d[identifiers.index("Accel/gyro self test") - 1] == None:
                        if output not in strings:        
                                d[identifiers.index("Accel/gyro self test") - 1] = True
                                # i.append(output)
                                print("Accel/gyro self test obtained...")
                                if output.find(gyro_pass_string) != -1: 
                                        strings[identifiers.index("Accel/gyro self test") - 1] = "Test Passed"
                                else:
                                        strings[identifiers.index("Accel/gyro self test") - 1] = "Test failed"
                #compass test
                if output.find("Compass self test") != -1 and d[identifiers.index("Compass self test") - 1] == None:
                        if output not in strings:        
                                d[identifiers.index("Compass self test") - 1] = True
                                # i.append(output)
                                print("Compass self test obtained...")
                                if output.find(comp_pass_string) != -1: 
                                        strings[identifiers.index("Compass self test") - 1] = "Test Passed"
                                else:
                                        strings[identifiers.index("Compass self test") - 1] = "Test failed"
                #barometer test
                if output.find("Barometer self test") != -1 and d[identifiers.index("Barometer self test") - 1] == None:
                        if output not in strings:        
                                d[identifiers.index("Barometer self test") -1] = True
                                # i.append(output)
                                print("Barometer self test obtained...")
                                if output.find(baro_pass_string) != -1: 
                                        strings[identifiers.index("Barometer self test") - 1] = "Test Passed"
                                else:
                                        strings[identifiers.index("Barometer self test") - 1] = "Test failed"

                #check if everything was taken in the amount of lines allowed to search
                if None not in d:
                        break
                else:
                        continue
        #check if there are missing identifiers
        n = 0
        for id in strings:
                try:
                        line += id +","
                        n += 1
                except TypeError:
                        line += "Failed to obtain,"
                        print("Failed to obtain " + identifiers[n])
                        n += 1
        line += "\n"
        dupe  = False
        for id in strings:
               dupe = id_search(logName, id)
        if dupe == False:
                log_writer(logName, line)
        else:
                print("***Current xtag already logged***")

                       
def id_search(file, id):
        f = open(file, "r")
        flag = False
        for line in f:
            try:
                if id in line:
                        flag = True
                        break
            except TypeError:
                break
        return flag


def main():
        if not os.path.exists(logName):
                log = open(logName, 'w+')
                log.write("SN,Tag GUID,IMEI,ICCID,MAC Address,Animal GUID,SDC Voltage,VBAT & VSOLAR,Cell FW Version,SW Version,Hash,Accel/gyro self test,Compass self test,Barometer self test\n")
                log.close()
        print("Started at " + datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        while True:
                ser.close()
                while True:
                        try:
                                print("Enter SN to continue: \n>", end="")
                                sn = input()
                                if sn == "" :
                                        raise ValueError
                                if id_search(logName, sn) == True:
                                        raise DupeError
                                break
                        except ValueError:
                                print("Invalid SN, try again\n")
                        except DupeError:
                                print("Previously logged SN, try again\n")
                print("SN recieved, connect xtag...")
                ser.open()
                ser_listen_and_log(sn)
                print("Press enter to continue, or enter \"e\" to end")
                a = input()
                if a == "e":
                        print("Logging ended: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
                        break


if __name__ == "__main__":
        while True:
                try:
                        print("Enter port: \n>", end="")
                        port = input()
                        ser = serial.Serial(port, 115200, timeout=10)
                        break
                except SerialException:
                        print("Invalid port, try again\n")
        if ser.isOpen():
                main()
        else:
                print("ERROR: CAN't OPEN CONNECTION")
        ser.close()
