# AEV sensor data collection functions

# author: Owen Bramley
# date modified: 04/10/2023
# version: 0.1 (alpha)


import board
import adafruit_ahtx0
import adafruit_adxl34x
import adafruit_gps
import busio


class Telemetry:

    def __init__(self):
        self.ic2 = board.I2C()
        self.eb_temp = None
        self.accel_data = None
        self.lat = None
        self.long = None
        # self.gps = adafruit_gps.GPS(busio.UART(board.TX, board.RX, baudrate=9600, timeout=30), debug=False)

        # self.gps.send_command(b'PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
        # self.gps.send_command(b'PMTK220,1000')

    def update_eb_temp(self):
        # Create sensor object, communicating over the board's default I2C bus
        sensor = adafruit_ahtx0.AHTx0(self.ic2)
        # update the current temperature of the EB Bay
        self.eb_temp = round(sensor.temperature, 1)

    def update_accel_data(self):
        # initialize I2C connection with the ADXL345 board
        data = adafruit_adxl34x.ADXL345(self.ic2).acceleration
        rounded = (f'{round(data[0], 2):.2f}', f'{round(data[1], 2):.2f}', f'{round(data[2], 2):.2f}')
        self.accel_data = ', '.join(rounded)

    def update_location(self):
        self.gps.update()
        if not self.gps.has_fix:
            print('Waiting for fix...')
        else:
            self.lat = self.gps.latitude
            self.long = self.gps.longitude

    def update_us_distance(self, sensor_id):
        # threshold for object detection
        distance_threshold = 2
        obj_detected = True

        if sensor_id == 1:
            return
        elif sensor_id == 2:
            return
        elif sensor_id == 3:
            return
        elif sensor_id == 4:
            return
        elif sensor_id == 5:
            return
        elif sensor_id == 6:
            return
        elif sensor_id == 7:
            return
        elif sensor_id == 8:
            return

        # get sensor data (try catch)
        # set obj_detected

        return obj_detected

    def update_all_sensors(self):
        self.update_eb_temp()
        self.update_accel_data()
        # self.update_location()
        # self.update_us_distance()

    def print_telemetry(self):
        print(f'EB TEMP: {self.eb_temp} C    ACCEL: {self.accel_data}    LAT/LONG: {self.lat}, {self.long}')
