import threading
from serial import Serial

BAUD_RATE = 115200
PORT = '/dev/ttyACM0'


class AEV:
    """
    Controls the AEV and communicates with the arduino. Sends commands to arduino and reads responses.
    """
    def __init__(self):
        self.gps = {
            'quality': 0,
            'lat': 0,
            'long': 0,
            'fix': 0,
        }
        self.accelerometer = '0,0,0'
        self.temp_c = 0
        self.ultrasonic_distance_cm = {
            'front': 0,
            'back': 0,
            'left': 0,
            'right': 0,
        }
        self.current_speed_mph = 0
        self.door_status = 'c'
        self.manual_control = False
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
                arduino_response = self.serial_comm.readline()
                if arduino_response:
                    res = arduino_response.decode().strip()
                    print(res)
        finally:
            self.__del__()

    def __del__(self):
        """
        Closes the serial port on program exit.
        """
        if self.serial_comm:
            self.serial_comm.close()
            print('Serial port closed')

    def telemetry_json(self):
        return {
            'gps': self.gps,
            'accelerometer': self.accelerometer,
            'temp_c': self.temp_c,
            'ultrasonic_distance_cm': self.ultrasonic_distance_cm,
            'current_speed_mph': self.current_speed_mph,
            'door_status': self.door_status,
            'manual_control': self.manual_control,
        }

    def update_telemetry(self):
        print('getting telem')
        self.send_command('<TELEMETRY>')

    def forward(self):
        print('sending forward...')
        self.send_command('<FORWARD>')

    def reverse(self):
        print('sending reverse...')
        self.send_command('<REVERSE>')

    def turn_left(self):
        print('sending left...')
        self.send_command('<LEFT>')

    def turn_right(self):
        print('sending right...')
        self.send_command('<RIGHT>')

    def forward_left(self):
        print('sending forward left...')
        self.send_command('<FORWARD_LEFT>')

    def forward_right(self):
        print('sending forward right...')
        self.send_command('<FORWARD_RIGHT>')

    def reverse_left(self):
        print('sending reverse left...')
        self.send_command('<REVERSE_LEFT>')

    def reverse_right(self):
        print('sending reverse right...')
        self.send_command('<REVERSE_RIGHT>')

    def stop(self):
        print('sending stop...')
        self.send_command('<STOP>')

    def headlights_on(self):
        print('sending headlights on...')
        self.send_command('<HEADLIGHTS_ON>')

    def headlights_off(self):
        print('sending headlights off...')
        self.send_command('<HEADLIGHTS_OFF>')
