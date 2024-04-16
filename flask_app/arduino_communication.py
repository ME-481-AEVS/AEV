import threading
from serial import Serial

BAUD_RATE = 115200
PORT = '/dev/ttyACM0'


class ArduinoCommunication:
    """
    Class to communicate with arduino. Sends commands and reads responses.
    """
    def __init__(self):
        try:
            self.serial_comm = Serial(PORT, BAUD_RATE)
            self.serial_comm.timeout = 1
            threading.Thread(target=self.read_response).start()
        except:
            print("Could not communicate with arduino.")
            exit(1)

    def send_command(self, command: str):
        """
        Send command to arduino and request response
        :param command: takes command in "<>" form
        """
        if command is None or command[0] != '<':
            return "Invalid command"
        command = command.strip()
        self.serial_comm.write((command + '\n').encode())

    def read_response(self):
        """
        Reads response from arduino.
        """
        print('Waiting for input from arduino...')
        try:
            while True:
                print(self.serial_comm.readline().decode())
        finally:
            self.__del__()

    def __del__(self):
        """
        Closes the serial port on program exit.
        """
        self.serial_comm.close()
        print('Serial port closed')
