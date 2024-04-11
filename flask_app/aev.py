from random import random
from arduino_communication import ArduinoCommunication


class AEV:
    def __init__(self):
        self.telemetry = {
            'elec_bay_temp_c': 0,
            'accel_data': 0,
            'lat': 0,
            'long': 0,
        }
        self.ard_comm = ArduinoCommunication()
        self.current_speed_mph = 0
        self.door_status = 'c'
        self.heartbeat = 0
        self.manual_control = False

    def update_telemetry(self):
        print('getting telem')
        # print(self.ard_comm.send_command('<TELEMETRY>'))
        self.telemetry = {
            'elec_bay_temp_c': random() * 100,
            'accel_data': random() * 100,
            'lat': random() * 100,
            'long': random() * 100,
        }

    def forward(self):
        print('sending forward...')
        self.ard_comm.send_command('<FORWARD>')

    def reverse(self):
        print('sending reverse...')
        self.ard_comm.send_command('<REVERSE>')

    def turn_left(self):
        print('sending left...')
        self.ard_comm.send_command('<LEFT>')

    def turn_right(self):
        print('sending right...')
        self.ard_comm.send_command('<RIGHT>')

    def forward_left(self):
        print('sending forward left...')
        self.ard_comm.send_command('<FORWARD_LEFT>')

    def forward_right(self):
        print('sending forward right...')
        self.ard_comm.send_command('<FORWARD_RIGHT>')

    def reverse_left(self):
        print('sending reverse left...')
        self.ard_comm.send_command('<REVERSE_LEFT>')

    def reverse_right(self):
        print('sending reverse right...')
        self.ard_comm.send_command('<REVERSE_RIGHT>')

    def stop(self):
        print('sending stop...')
        self.ard_comm.send_command('<STOP>')

    def headlights_on(self):
        print('sending headlights on...')
        self.ard_comm.send_command('<HEADLIGHTS_ON>')

    def headlights_off(self):
        print('sending headlights off...')
        self.ard_comm.send_command('<HEADLIGHTS_OFF>')
