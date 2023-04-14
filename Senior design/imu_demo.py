#by Ethan B @6:01PM

import numpy as np
import time
import serial
import struct, matplotlib.pyplot as plt, collections
from matplotlib.animation import FuncAnimation

port = serial.Serial('COM14',baudrate=9600)

xdata = collections.deque(np.zeros(10))

ydata = collections.deque(np.zeros(10))

zdata = collections.deque(np.zeros(10))

def update(i):
    first_byte = (port.read()).decode('utf-8')
    if (port.in_waiting > 0) and ( first_byte == '<'):
        data = []
        b = []
        axis = 0
        while(1):
            current_byte = port.read().decode('utf-8')
            
            if current_byte == ':':
                val = ''
                for char in b:
                    val += char
                data.append(val)
                ++axis
                b.clear() 
            
            elif current_byte == '>':
                try:
                    x = float(data[0])
                    y = float(data[1])
                    z = float(data[2])
                    print(x, y, z)
                except:
                    break
                xdata.popleft()
                xdata.append(x)    
                ydata.popleft()
                ydata.append(y)
                zdata.popleft()
                zdata.append(z)
                
                ax.cla()
                
                ax.plot(xdata)
                ax.scatter(len(xdata)-1, xdata[-1])
                ax.text(len(xdata)-1, xdata[-1]+2, "{} X".format(xdata[-1]))
                ax.set_ylim(-5,5)
                
                ax.plot(ydata)
                ax.scatter(len(ydata)-1, ydata[-1])
                ax.text(len(ydata)-1, ydata[-1]+2, "{} Y".format(ydata[-1]))
                ax.set_ylim(-5,5)
                
                ax.plot(zdata)
                ax.scatter(len(zdata)-1, zdata[-1])
                ax.text(len(zdata)-1, zdata[-1]+2, "{} Z".format(zdata[-1]))
                ax.set_ylim(-5,5)
                plt.xlabel("Time",fontsize=15)
                plt.ylabel("Value",fontsize=15)
                plt.title("ADXL377")
                time.sleep(0.05)
                break
                
            else:
                b.append((current_byte))


fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot()
plt.xlabel("Time", fontsize=15)
plt.ylabel("Value", fontsize=15)
plt.title("ADXL377")
ax.set_facecolor('#DEDEDE')

ani = FuncAnimation(fig, update, interval=1)
plt.show()


# for debug of update func
# while(1):
#     update(1)
    
    