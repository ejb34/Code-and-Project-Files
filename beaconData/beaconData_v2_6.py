import time
import subprocess
from datetime import datetime
import codecs
import os.path
# example: 
# May 20 13:01:14  Device 58:93:D8:17:01:67 ServiceData Value:
# May 20 13:01:14   35 2e 38 36 2c 34 2e 31 33                       5.86,4.13    

# ---text ui for doing specific timings (START)--- 
# print("Enter \"Timed\" to set a number of hours to run, or enter anything else to run infinitely \n > ", end = '')
# choice = input()
# timedMode = True
# if (choice.lower() == "timed" or choice.lower() == "time"):
#     timedMode = True
#     print("Enter run time in hours\n > ", end = '')
#     runTime = float(input())
# else:
#     timedMode = False
#
# ---text ui for doing specific timings (END)---
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
if not (os.path.exists( os.path.dirname(os.path.abspath(__file__)) + "/log0.txt")):        
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log0.txt", "w+") as log:
        log.write("")
        log.close
if not (os.path.exists( os.path.dirname(os.path.abspath(__file__)) + "/log1.txt")):        
    with open(os.path.dirname(os.path.abspath(__file__)) + "/log1.txt", "w+") as log:
        log.write("")
        log.close
if not (os.path.exists( os.path.dirname(os.path.abspath(__file__)) + "/dataLog.txt")):        
    with open(os.path.dirname(os.path.abspath(__file__)) + "/dataLog.txt", "w+") as log:
        log.write("")
        log.close
if not (os.path.exists( os.path.dirname(os.path.abspath(__file__)) + "/CSVs/")):        
    os.mkdir((os.path.dirname(os.path.abspath(__file__)) + "/CSVs/"))
if not (os.path.exists( os.path.dirname(os.path.abspath(__file__)) + "/bt.sh")):        
    with open(os.path.dirname(os.path.abspath(__file__)) + "/bt.sh", "w+") as log:
        log.write("bluetoothctl scan on | ts > " + os.path.dirname(os.path.abspath(__file__)) + "/log0.txt" " &\n"
                  "sleep 300\n"
                  "killall bluetoothctl\n"
                  "sleep 10")
        log.close
    subprocess.run(["chmod", "+x", os.path.dirname(os.path.abspath(__file__)) + "/bt.sh"])

print("started: " + dt_string)
print("running...")
tagList = []

# Main loop
while 1:

 #---Timed-Mode loop break (START)---
    # if(timedMode):
    #     currentTime = time.time()
    #     if((currentTime - startTime) >= (runTime * (60**2))):
    #         break
 #---Timed-Mode loop break  (END)---
    subprocess.run(["killall", "bluetoothctl"])
    try:
        addr = "58:93:D8"
        time.sleep(2)
        subprocess.run([os.path.dirname(os.path.abspath(__file__)) + "/bt.sh"], shell=True)
        data0 = open(os.path.dirname(os.path.abspath(__file__)) + "/log0.txt", "r")

        with open(os.path.dirname(os.path.abspath(__file__)) + "/log1.txt", "w") as data1:   
            for line in data0:
                if (line.find(addr) != -1) and ((line.find("ServiceData Value") != -1) or (line.find("RSSI") != -1)):
                
                    line = line.replace("[[0;93mCHG[0m]", "")
                    data1.write(line)
                    nextline = data0.readline()
                    if (nextline.find("Device") == -1):
                            data1.write(nextline)
                            data1.close
        data0.close
    # look through log1.txt and writes to dataLog.txt
        log = open(os.path.dirname(os.path.abspath(__file__)) + "/log1.txt", "r")
        tagList = []
        for line in log:
            if line.find("58:93:D8") != -1:
                s2 = line[24:41]
                s = line[0:15]
                same = False
                for mac in tagList:
                    if s == mac:
                        same = True
                if same == False:
                    tagList.append(s) 
                nextLine = log.readline()
                if line.find("RSSI") != -1: 
                    rssi = line[48:51]
                    with open("beaconData/dataLog.txt", "a") as data:
                        data.write( s + "," + s2 + "," + "," + "," + "," + rssi + "\n")
                        data.close
                else:
                    hex = nextLine[18:44].replace(" ", "")
                    hexStr = (str(codecs.decode(hex, "hex")).replace("\'", "")).replace("b","")
                    if hexStr.find(",") != -1:
                        with open("beaconData/dataLog.txt", "a") as data:
                                data.write( s + "," + s2 + "," + hexStr + "," + "," + "\n")
                                data.close
                    else:
                        with open("beaconData/dataLog.txt", "a") as data:
                                data.write( s + "," + s2 + "," + "," + "," + hexStr + "," + "\n")
                                data.close

        log.close

    # look through dataLog.txt
        tagList2 = []
        dataLog = open(os.path.dirname(os.path.abspath(__file__)) + "/dataLog.txt", "r")
        for line in dataLog:
                if line.find("58:93:D8") != -1:
                    s2 = line[16:33]
                    same = False
                    for mac in tagList2:
                        if s2 == mac:
                            same = True
                    if same == False:
                        tagList2.append(s2)
        dataLog.close
    # Writing to .csv
        for mac in tagList2:
            hasFile = False
            log = open(os.path.dirname(os.path.abspath(__file__)) + "/dataLog.txt", "r") 
            dataList = []
            for line in log:
                if line.find(mac) != -1:
                    dataList.append(line)
            # Create CSV  
            if not (os.path.exists(os.path.dirname(os.path.abspath(__file__)) + "/CSVs/" + mac + ".csv")):        
                with open(os.path.dirname(os.path.abspath(__file__)) + "/CSVs/" + mac + ".csv", "w+") as table:
                    table.write("Time,MAC Addr,Panel,Battery,Heading,RSSI,Lat,Lon \n")
                    table.close
            # Write
            for data in dataList:
                with open(os.path.dirname(os.path.abspath(__file__)) + "/CSVs/" + mac + ".csv", "a") as table:               
                    table.write(str(data))
                    table.close
            log.close
            
    
    # Clearing logs
        with open(os.path.dirname(os.path.abspath(__file__)) + "/dataLog.txt", "w") as oldLog:
            oldLog.write("")
        oldLog.close
        with open(os.path.dirname(os.path.abspath(__file__)) + "/log1.txt", "w") as oldLog:
            oldLog.write("")
        oldLog.close
    except KeyboardInterrupt:
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        subprocess.run(["killall", "bluetoothctl"])
        print("\nstopped: " + dt_string)
        break