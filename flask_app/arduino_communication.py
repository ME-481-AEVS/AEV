"""
Purpose: This class is used to communicate with the Arduino using the serial port.
The program sends a command to the Arduino and then waits for a response.
Authors: Owen Bramley, Christian Komo, Rob Godfrey
"""

from serial import Serial

BAUD_RATE = 115200
PORT = '/dev/ttyACM0'
# LOGFILE = f'logs/datalog{str(time.time())}.txt'


class ArduinoCommunication:
    def __init__(self):
        try:
            self.serial_comm = Serial(PORT, BAUD_RATE)
            self.serial_comm.timeout = 1
        except:
            print("Could not communicate with arduino.")
            exit(1)

    def send_command(self, command='0', log=False):
        """
        Send command to arduino and request response
        :param command: takes command in "<>" form
        :param log: log data on/off
        """
        i = command.strip()
        if i == '0':
            return "Invalid command"
        self.serial_comm.write((i + '\n').encode())
        """
        # read the response from the Arduino
        try:
            if (log):
                # log data received from the Arduino if log is True
                # file = open(LOGFILE, "w")
                # file.write(self.serial_comm.readline().decode('ascii'))
                pass

            print(self.serial_comm.readline().decode('ascii'))
        except:
            file = open(LOGFILE, "a")
            file.write("Error")  # caught errors added to log
        """

    def __del__(self):
        """
        Close the serial port on program exit
        """
        self.serial_comm.close()
        print('Serial port closed')
