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
        # update with random values for now
        print(self.ard_comm.send_command('<TELEMETRY>'))
        self.telemetry = {
            'elec_bay_temp_c': random() * 100,
            'accel_data': random() * 100,
            'lat': random() * 100,
            'long': random() * 100,
        }

    def forward(self):
        print('sending forward...')
        print(self.ard_comm.send_command('<FORWARD>'))

    def stop(self):
        print('sending stop...')
        print(self.ard_comm.send_command('<STOP>'))

