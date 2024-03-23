from random import random


class AEV:
    def __init__(self):
        self.telemetry = {
            'elec_bay_temp_c': 0,
            'accel_data': 0,
            'lat': 0,
            'long': 0,
        }
        self.current_speed_mph = 0
        self.door_status = 'c'
        self.heartbeat = 0
        self.manual_control = False

    def update_telemetry(self):
        # update with random values for now
        self.telemetry = {
            'elec_bay_temp_c': random() * 100,
            'accel_data': random() * 100,
            'lat': random() * 100,
            'long': random() * 100,
        }
