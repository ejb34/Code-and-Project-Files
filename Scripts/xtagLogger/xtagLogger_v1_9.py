#This is manual injection of the XTRA data by downloading it form the internet to the Pi
#and then applying it to the module.

from genericpath import exists
import serial
import time
from datetime import datetime
import os
import subprocess
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
Time = str(time.strftime('%Y-%m-%d'))
logName = "C:\\xtag_MFG_INFO\\MFG_TST_INFO\\"+Time+".csv"
server = "C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\GUID\\LwM2M\\100_server.psk"
class DupeError(Exception):
        '''random exeption to catch a duplication error '''
        pass


# Strings to pull from the output, AFTER white space has been stripped

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

# list used for the index of certain strings, in the order presented on the .csv file

identifiers = ["SN","Tag GUID","IMEI","ICCID","MAC Address","Animal GUID",
        "SDC Voltage","VBAT & VSOLAR","Cell FW Version","SW Version","Hash","Cell Module Functional", "Accel/gyro self test",
        "Compass self test","Barometer self test"] 


def log_writer(file_name, input):
        '''writes to file'''
        log = open(file_name,'a',newline='')
        log.write(input)
        log.close()

def msisdn_writer(guid, imei, msisdn):
        file = open("C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\" + guid + "\\LwM2M\\100_server.psk" , "w+")
        file.write("|urn:IMEI-MSISDN:" + imei + "-" + msisdn + "|:d6160c2e7c90399ee7d207a22611e3d3a87241b0462976b935341d000a91e747")
        file.close()

def ser_listen_and_log(sn):

        '''listens to the serial input (utf-8) and writes the collected data in a 
                specific order to the continued or newly created .csv file.'''
        


        # contains the actual data strings to be written to the .csv file after modification. 
        strings = [None] * 14
        strings[0] = sn
        # instantiate line string so it can be appended to at the end of the data collection.
        line = ""
        logNameOutput = "C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\GUID" + sn +"\\MFG_TST_OUTPUT\\output.txt"
        indivDir= ["\\xtag_MFG_INFO\\xtag_INDV_INFO\\GUID" + sn +"\\", "C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\GUID" + sn + 
                "\\LwM2M\\", "\\xtag_MFG_INFO\\xtag_INDV_INFO\\GUID" + sn + "\\MFG_TST_OUTPUT\\"]
        makeDir(indivDir)
        # the range indicates the number of output lines to be read.
        for x in range(0, 80):
                try:        
                        output = str(ser.readline().decode('utf-8'))
                except UnicodeDecodeError:
                        output = ""

                # all selection statments function esentially the same, checking if a identifying phrase is contained in the output and 
                # editing the output so that all the desirable info is retained, and nothing more.

                # 'strings[identifiers.index("Tag GUID")]', for example is checking if the tag guid has already been recorded, as well as adding it to the specified index position. 
                # This is to prevent unnecessary repitition and re writing over already obtained data.

                # Write to 'all' output file
                log_writer(logNameOutput,output)

                #tag guid
                if output.find("Tag GUID") != -1 and strings[identifiers.index("Tag GUID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(tGUID_String,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:
                                print("Tag GUID obtained...")
                                strings[identifiers.index("Tag GUID")] = output
                                new_guid_path = "C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\" + str(strings[identifiers.index("Tag GUID")]) + "\\"
                                new_guid_output_path = new_guid_path + "MFG_TST_OUTPUT\\" + str(strings[identifiers.index("Tag GUID")]) + "_output.txt"
                                try:
                                        os.rename(indivDir[0], new_guid_path)
                                        os.rename(new_guid_path +"\\MFG_TST_OUTPUT\\output.txt", new_guid_output_path)
                                        logNameOutput = new_guid_output_path
                                except FileExistsError:
                                        pass
                #animal guid
                if output.find("Animal GUID") != -1 and strings[identifiers.index("Animal GUID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(aGUID_String,"")
                        output = output.replace("\n","")
                        if output not in strings:
                                print("Animal GUID obtained...")
                                strings[identifiers.index("Animal GUID")] = output
                #IMEI
                if output.find("IMEI") != -1 and strings[identifiers.index("IMEI")] == None:
                        output = output.replace(" ","")
                        output = output.replace(imei_String,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:        
                                print("IMEI obtained...")
                                strings[identifiers.index("IMEI")] = output
                #ICCID
                if output.find("ICCID") != -1 and strings[identifiers.index("ICCID")] == None:
                        output = output.replace(" ","")
                        output = output.replace(iccid_String,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:        
                                print("ICCID obtained...")
                                strings[identifiers.index("ICCID")] = output
                #mac address
                if output.find("MAC") != -1 and strings[identifiers.index("MAC Address")] == None:
                        output = output.replace(" ","")
                        output = output.replace(bt_String,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:
                                print("MAC address obtained...")
                                strings[identifiers.index("MAC Address")] = output
                #SDC voltage
                if output.find("SDC Voltage Good:") != -1 and strings[identifiers.index("SDC Voltage")] == None:
                        output = output.replace(" ","")
                        output = output.replace(v_String,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:
                                print("SDC Voltage obtained...")
                                strings[identifiers.index("SDC Voltage")] = output
                #VBAT VSOLAR
                if output.find("VBAT") != -1 and strings[identifiers.index("VBAT & VSOLAR")] == None:
                        output = output.replace(" ","")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        output = output.replace("VBAT=", "")
                        output = output.replace("SOLAR=", "")
                        output = output.replace("V", ",")
                        if output not in strings:
                                print("VBAT & VSOLAR obtained...")
                                strings[identifiers.index("VBAT & VSOLAR")] = output
                #cell fw
                if output.find("Cell FW Version") != -1 and strings[identifiers.index("Cell FW Version")] == None:
                        output = output.replace(" ","")
                        output = output.replace(cellfw_string,"")
                        output = output.replace("\n","")
                        output = output.replace("\t","")
                        if output not in strings:        
                                print("Cell FW Version obtained...")
                                strings[identifiers.index("Cell FW Version")] = output
                #sw version and hash
                if output.find("SW Version") != -1 and strings[identifiers.index("SW Version")] == None:
                        output = output.replace(" ","")
                        output = output.replace(sw_string,"")
                        output = output.replace(hash_string,"")
                        output = output.replace("\t","")
                        output = output.replace("\n","")
                        if output not in strings:        
                                print("SW Version obtained...")
                                strings[identifiers.index("SW Version")] = output
                #cell module test
                if output.find("Failed to find \'+cclk\'") != -1 or output.find("Failed to query IMEI!") != -1:
                        print("Cell module not functional...")
                        strings[identifiers.index("Cell Module Functional") - 1] = "No"
                else:
                        strings[identifiers.index("Cell Module Functional") - 1] = "Yes"

                #gyro test
                if output.find("Accel/gyro self test") != -1 and strings[identifiers.index("Accel/gyro self test") - 1] == None:
                        print("Accel/gyro self test obtained...")
                        if output.find(gyro_pass_string) != -1: 
                                strings[identifiers.index("Accel/gyro self test") - 1] = "Passed"
                        else:
                                strings[identifiers.index("Accel/gyro self test") - 1] = "Failed"
                #compass test
                if output.find("Compass self test") != -1 and strings[identifiers.index("Compass self test") - 1] == None:
                        print("Compass self test obtained...")
                        if output.find(comp_pass_string) != -1: 
                                strings[identifiers.index("Compass self test") - 1] = "Passed"
                        else:
                                strings[identifiers.index("Compass self test") - 1] = "Failed"
                #barometer test
                if output.find("Barometer self test") != -1 and strings[identifiers.index("Barometer self test") - 1] == None:
                        print("Barometer self test obtained...")
                        if output.find(baro_pass_string) != -1: 
                                strings[identifiers.index("Barometer self test") - 1] = "Passed"
                        else:
                                strings[identifiers.index("Barometer self test") - 1] = "Failed"

        msisdn_writer(strings[identifiers.index("Tag GUID")],strings[identifiers.index("IMEI")],"xxxxxxxxxx")
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

                       
def id_search(file, s):

        '''returns true if the string is found int the file'''
        
        f = open(file, "r")
        flag = False
        for line in f:
            try:
                if s in line:
                        flag = True
                        break
            except TypeError:
                break
        return flag


#GUID\\MFG_TST_OUTPUT\\

def makeDir(paths):
        for path in paths:
                if not os.path.exists(path):
                        os.mkdir(path)


def main():
        startingDir = ["C:\\xtag_MFG_INFO\\", "C:\\xtag_MFG_INFO\\MFG_TST_INFO\\", "C:\\xtag_MFG_INFO\\xtag_INDV_INFO\\"]
        makeDir(startingDir)

        if not os.path.exists(logName):
                log = open(logName, 'w+')
                log.write("SN,Tag GUID,IMEI,ICCID,MAC Address,Animal GUID,SDC Voltage,VBAT,VSOLAR,Cell FW Version,SW Version,Hash,Cell Module Functional,Accel/gyro self test,Compass self test,Barometer self test\n")
                log.close()
        else:
                print("\nContinuing "+Time+" log")
                time.sleep(1)


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
                ###change filename
               # All = subprocess.Popen(args=["python", ".\\xtagLogger\\xtagLoggerALL_v0_1.py"])
                ser_listen_and_log(sn)
                print("Press enter to continue, or enter \"e\" to end: \n", end="")
                a = input()
                if a == "e":
                      #  All.terminate()
                        print("Logging ended: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n")
                        break
                if KeyboardInterrupt:
                      #  All.terminate()
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
                print("ERROR: CAN'T OPEN CONNECTION")
        ser.close()
