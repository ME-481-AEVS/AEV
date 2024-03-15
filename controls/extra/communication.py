# TEAM WAEVS
# Date: 02/20/2021
# Purpose: This program is used to communicate with the Arduino using the serial port.
# The program sends a command to the Arduino and then waits for a response.
# Authors: Owen Bramley, Christian Komo

import serial
import time

# open communication to the serial port of the Arduino 
BAUDRATE = 115200
PORT = '/dev/cu.usbmodem101'
LOGFILE = "datalog.txt"

try:
    serialcomm = serial.Serial(PORT, BAUDRATE)
    serialcomm.timeout = 1
except:
    print("Could not communicate with arduino. Check the port and baudrate.")
    exit() # exit the program if the serial port cannot be opened

def sendCommand(command = '0', log = False):
    i = command.strip()
    if i == '0':
        return "Invalid command"
    serialcomm.write(i.encode())
    time.sleep(0.5)
    # read the response from the Arduino
    if (Log):
        file = open(LOGFILE, "a")
        file.write(serialcomm.readline().decode('ascii'))
    print(serialcomm.readline().decode('ascii'))
    serialcomm.close()
    return "Complete" # close the serial port


# log data recived from the Arduino


# catch any errors that may occur and add them to the log

