import time
import serial, threading
import os, imu_vis
from datetime import datetime


sen_max_duration = 7


while(1):
    try:
        port = serial.Serial('COM6',baudrate=9600, timeout=1)
        break
    except:
        print("Could not connect to reciever, trying again...")
        time.sleep(1)

cap_num = 0
while(1):
    # try:

    #debug
        print(f'Select number of sensors to use *using both sensors will results in more precise data but half as many data points* (1 - 2):\n>', end='')
        sensorcount = input()
        try:
            int(sensorcount)
            if int(sensorcount) not in range(1,3):
                print('ERROR: Invalid value')
                continue
        except:
            print('ERROR: Invalid input')
            continue

        while(1):
            print(f'Enter the desired capture duration in whole seconds (1 - {int(sensorcount)*sen_max_duration}):\n>', end='')
            duration = input()
            try:
                int(duration)
            except:
                print('ERROR: Invalid input')
                continue
            if (sensorcount == '1') and (int(duration) not in range(1,(sen_max_duration+1))):
                print('ERROR: Invalid duration')
                continue
            if (sensorcount == '2') and (int(duration) not in range(1,(2*sen_max_duration)+1)):
                print('ERROR: Invalid duration')
                continue
            break
        
        while(1):
            print(f'Capturing for {duration}s... this capture will contain approx. {(int(duration) * (834/int(sensorcount)))*9} data points. Is this ok? (y/n)\n>', end='')
            confirm = input().lower()
            if confirm == 'y' or confirm == 'n':
                break
            print("ERROR: Invalid input\n>", end='')
        
        if confirm == 'n':
            print("Capture cancelled...")
            time.sleep(1)
            continue
        now = datetime.now()
        fp = "logs/" + now.strftime("%Y-%m-%d_%H-%M-%S") + '.csv'
        with open(fp, 'w+') as file:
            file.write('Acc x (mg) ,Acc y (mg) ,Acc z (mg) ,Gyr x (DPS) ,Gyr y (DPS) ,Gyr z (DPS) ,Mag x (uT) ,Mag y (uT) ,Mag z (uT) , Time (ms) \n')
        print("Created log file...")
        
        print(f"Ready for {duration}s capture, press enter to start:\n>", end='')
        input()
        print("Capturing in 3...")
        time.sleep(1)
        print("Capturing in 2...")
        time.sleep(1)
        print("Capturing in 1...")
        time.sleep(1)
        print("Capturing...Please wait")
        
        port.write(sensorcount.encode('utf-8'))
        time.sleep(1) 
        port.write(duration.encode('utf-8'))
       
        while(1):
            first_line = port.readline().decode('utf-8')
            if '!' in first_line: 
                break
        while(1):
            print('Capture Completed! Transfer and write data to log? (y/n)\n>', end='')
            confirm = input().lower()
            if confirm == 'y' or confirm == 'n':
                break
            print("ERROR: Invalid input")
        
        if confirm == 'n':
            print("Data transfer cancelled...")
            port.write('2'.encode('utf-8'))
            time.sleep(1)
            continue    
        
        print('Transferring data... please wait...')
        port.write('1'.encode('utf-8'))

        with open(fp, 'a') as file:
            while(1):    
                i = 0
                try:
                    byte = port.read().decode('utf-8')
                    line = port.readline().decode('utf-8')
                    if byte == '<':
                        file.write(line)
                        print(line)
                        continue
                    elif 'ovf' in line:
                        print("Error in collecting data (ovf)")
                        break
                    elif '>' in line: 
                            print('Data succesfully transferred!')
                            time.sleep(1)
                            break
                except:
                    continue
        p = threading.Thread(target=imu_vis.plot(fp))
        p.start()
    # except:
    #     print("ERROR: Lost connection")