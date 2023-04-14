import time
import serial
import numpy as np
import struct, matplotlib.pyplot as plt, collections
import os,pathlib
import os
port = serial.Serial('COM14',baudrate=9600)

cap_num = 0
fp = 'cap' + str(cap_num) + '.csv'
with open(fp, 'w+') as file:
     file.write('X,Y,Z\n')


while(1):
    #if connection is severed and malformed packet is read
    try:
        first_byte = (port.read()).decode('utf-8')
    except:
        continue
    if (port.in_waiting > 0) and ( first_byte == '<'):
        data = []
        b = []
        axis = 0
        while(1):
            try:
                #if connection is severed and malformed packet is read
                current_byte = port.read().decode('utf-8')
            except:
                break
            if current_byte == ':':
                val = ''
                for char in b:
                    val += char
                data.append(val)
                ++axis
                b.clear() 
            
            elif current_byte == '>':
                try:
                    # These valus are mainly used for calculations, but there aren't
                        # any in this script; it just writes to a file.
                    x = float(data[0])
                    y = float(data[1])
                    z = float(data[2])
                    
                    print(x,y,z)
                    with open(fp, 'a') as file:
                        file.write(data[0] +','+ data[1] +','+ data[2] + '\n')
                    time.sleep(0.05)
                except:
                    break
    
                break
                
            else:
                b.append((current_byte))