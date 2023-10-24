import time
import serial, threading
import os, imu_vis

while(1):
    try:
        port = serial.Serial('COM6',baudrate=9600, timeout=1)
        break
    except:
        print("Could not connect to reciever, trying again...")
        time.sleep(1)

cap_num = 0
while(1):
    try:
    #debug
        # port.write('200'.encode('utf-8'))
        # port.write('1'.encode('utf-8'))
        # while(1): 
        #     line = port.readline()
        #     print(line)
    #debug
        print('Enter the desired capture duration in whole seconds (1 - 10):\n>', end='')
        duration = input()
        try:
            int(duration)
        except:
            print('ERROR: Invalid input')
            continue
        if int(duration) not in range(1,10):
            print('ERROR: Invalid data point value')
            continue
        
        
        print(f'Capturing for {duration}s... this capture will contain approx. {duration * 834} data points. Is this ok? (y/n)\n>', end='')
        while(1):
            confirm = input().lower()
            if confirm == 'y' or 'n':
                break
            print("ERROR: Invalid input\n>", end='')
        
        if confirm == 'n':
            print("Capture cancelled...")
            time.sleep(1)
            continue
        
        fp = 'cap' + str(cap_num) + '.log'
        with open(fp, 'w+') as file:
            file.write('(Scaled xyz) , Acc (mg) ,  Gyr (DPS) , Mag (uT) , Time (ms) \n')
        print("Created log file...")
        
        print(f"Ready for {duration}s capture, press enter to start:\n>", end='')
        input()
        print("Capturing in 3...")
        time.sleep(1)
        print("Capturing in 2...")
        time.sleep(1)
        print("Capturing in 1...")
        time.sleep(1)
        print("Capturing...")
        port.write(duration.encode('utf-8'))
        while(1):
            first_line = port.readline().decode('utf-8')
            if '!' in first_line: 
                print('Capture Completed! Transfer and write data to log? (y/n)\n>', end='')
                break
        while(1):
            confirm = input().lower()
            if confirm == 'y' or 'n':
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
                        
                    elif 'T' in line: 
                            cap_num+=1
                            file.write(line)
                            print('Data succesfully transferred!')
                            time.sleep(1)
                            p = threading.Thread(target=imu_vis.plot(fp))
                            p.start()
                            break
                except:
                    continue
    except:
        print("ERROR: Lost connection")