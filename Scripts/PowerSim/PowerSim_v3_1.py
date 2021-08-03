
from logging import Logger
import time
from datetime import datetime
import math
from random import random
from bk_precision import PowerSupply
import subprocess
import os
import sys
import logger
def sunWave(x, amplitude):

    "Calculates a value for the wave, given an x input value"

    return (float(amplitude) * math.sin((8 * math.pi) * float(x)) + float(amplitude))
    
def sunWaveX(v, amplitude):

    "Returns the x value of the sine wave for the given v/y value"

    return math.asin((float(v) - float(amplitude)) / float(amplitude)) / (8 * math.pi)

def randomXPoint(minValue, maxValue):

    "Creates a random value withing a given range"

    return (float(minValue) + (random() * (float(maxValue) - float(minValue))))

def timeToLoop(t):

    "Converts input time t to the loop duration"

    return ((float(t) * 60**2) / 6) * 0.02

def psuLogger(ps):

    """ Logs Power Supply V and A """

    if not os.path.exists("PowerSim/logs/PSU.csv"):
        with open("PowerSim/logs/PSU.csv", "w+") as file:
            file.write("Time,PSU Voltage,PSU Current\n")
            file.close
    now = datetime.now()
    s =  now.strftime("%d/%m/%Y %H:%M:%S") + "," + (str(ps.readValues())).replace("(", "").replace(")", "").replace("True", "")
    with open("PowerSim/logs/PSU.csv", "a") as file:
        file.write(s + "\n")
        file.close

def fakeSunSimple(duration, startingV, V):

    "Simulates voltage over a period of time with one V value"

    now = datetime.now()
    print("Simulation started at: " + now.strftime("%d/%m/%Y %H:%M:%S" + "\n"))
    # Initailize powersupply unit from bk_precision
    ps = PowerSupply('/dev/ttyUSB0',vLim=60, cLim=3, baudrate=9600)
    ps.setVolt(startingV)
    ps.ON()
    i = 0
    #Main loop
    logger = subprocess.Popen(["python3", "PowerSim/logger.py"])
    print("running...")
    while i < timeToLoop(duration): 
        ps.setVolt(V) 
        ps.ON()
        psuLogger(ps)
        time.sleep(6)
        i += 0.02
    logger.kill() 


def fakeSun(duration, startingV, amplitude, high, low):

    """Simulates voltage over a period of time with 3 time phases:

            Phase 1 | High sunglight/power 

            Phase 2 | Low sunlight/power

            Phase 3 | Wave-based sunlight/power 
                                                                """

    now = datetime.now()
    print("Simulation started at: " + now.strftime("%d/%m/%Y %H:%M:%S" + "\n"))
    #Initailizes powersupply unit from bk_precision
    ps = PowerSupply('/dev/ttyUSB0',vLim=60, cLim=3, baudrate=9600)
    ps.setVolt(startingV)
    ps.ON()
    i = 0
    # Main loop
    logger = subprocess.Popen(["python3", "PowerSim/logger.py"])
    print("running...")
     
    #simulates high sunlight/power
    t = timeToLoop(duration)

    while(i < (t * 0.333333)):
        ps.setVolt(high) 
        ps.ON()
        psuLogger(ps)
        time.sleep(6)
        i += 0.02
        if i > timeToLoop(duration):
            break
    #simulates low sunglight/power
    while(i < (t * 0.666667)):
        ps.setVolt(low) 
        ps.ON()
        psuLogger(ps)
        time.sleep(6)
        i += 0.02
        if i > timeToLoop(duration):
            break
    #simulates wave-based sunlight/power
    while(i < t):            
        v = sunWave(i, amplitude)
        ps.setVolt(v) 
        ps.ON()
        psuLogger(ps)
        time.sleep(6)
        i += 0.02
        if i > timeToLoop(duration):
            break
    logger.kill() 

def run():

    if not os.path.exists("PowerSim/logs/"):
        os.mkdir("PowerSim/logs/")

    while True:
        print("Enter 1 for a single value simluation, enter 2 for a multi-value simulation:\n" + "> ", end = "")
        try:
            c = int(input())
        except ValueError:
            print("\n***Invalid Input***\n")
            continue
        if c == 2:
            while True:
                try:
                    print("Enter Maximum Simulation Voltage:\n" + "> ", end = "")
                    amplitude = float(input()) / 2
                    print("Enter High Power Simulation Voltage:\n" + "> ", end = "")
                    high = float(input())  
                    print("Enter Low Power Simulation Voltage:\n" + "> ", end = "")
                    low = float(input())
                    print("Enter Duration of Simulation In Hours:\n" + "> ", end = "")
                    duration = float(input()) 
                    break                    
                except ValueError:
                        print("\n***Invalid Input***\n")
                        continue
            fakeSun(duration, 1, amplitude, high, low)
            now = datetime.now()    
            print("\nSimulation finished at: " + now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
            break 
        if c == 1:
            while True:
                try:
                    print("Enter Simulation Voltage:\n" + "> ", end = "")
                    v = float(input())
                    print("Enter Duration of Simulation In Hours:\n" + "> ", end = "")
                    duration = float(input())
                    break       
                except ValueError:
                        print("\n***Invalid Input***\n")
                        continue
            fakeSunSimple(duration, 1, v)
            now = datetime.now()    
            print("\nSimulation finished at: " + now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
            break 
        else:
            print("\n***Invalid Input***\n")
            continue

try:
    sys.exit(run())
except KeyboardInterrupt:
    now = datetime.now()    
    print("\nSimulation stopped at: " + now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
    pass
except RuntimeError:
    now = datetime.now()    
    print("\nSimulation stopped at: " + now.strftime("%d/%m/%Y %H:%M:%S") + "\n")
    pass

# fakeSun(2,1,4,3,.5)
# fakeSunSimple(2,1,3)
