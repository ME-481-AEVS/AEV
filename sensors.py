# AEV sensor data collection functions

# author: Owen Bramley
# date modified: 04/10/2023
# version: 0.1 (alpha)


import time
import board
import neopixel_spi as neopixel
import adafruit_ahtx0
import adafruit_adxl34x


class Sensors:

    def __init__(self):
        self.pixels = neopixel.NeoPixel_SPI(board.SPI(), 150)
        self.ic2 = board.I2C()
        self.eb_temp = None
        self.accel_data = None
        self.coordinates = None
        self.fake_coor_index = 0

    def update_eb_temp(self):
        # Create sensor object, communicating over the board's default I2C bus
        sensor = adafruit_ahtx0.AHTx0(self.ic2)
        # update the current temperature of the EB Bay
        self.eb_temp = sensor.temperature

    def update_accel_data(self):
        # initialize I2C connection with the ADXL345 board
        return adafruit_adxl34x.ADXL345(self.ic2).acceleration

    def update_location(self):
        fake_coordinates = [
            (21.3000, -157.8175), (21.3001, -157.8175), (21.3002, -157.8175),
            (21.3003, -157.8175), (21.3004, -157.8175), (21.3005, -157.8175),
            (21.3006, -157.8176), (21.3007, -157.8177), (21.3007, -157.8178),
            (21.3006, -157.8178), (21.3006, -157.8178), (21.3005, -157.8177),
            (21.3004, -157.8176), (21.3003, -157.8176), (21.3001, -157.8175),
        ]
        self.coordinates = fake_coordinates[self.fake_coor_index]
        self.fake_coor_index += 1
        if self.fake_coor_index > len(fake_coordinates):
            self.fake_coor_index = 0

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

    def lights(self, state: int):
        """
        Changes the state of the neopixel warning lights.

        :param int state: The new state of the warning lights:
            0: off
            1: solid
            2: Flashing
        """
        if state == 1:
            # Fill all pixels yellow
            print('Turning all pixels on, solid yellow')
            self.pixels.fill((0, 255, 0))
            self.pixels.show()
        elif state == 2:
            # Flash lights
            print('Flashing pixels five times, solid yellow')
            self.pixels.fill((0, 255, 0))

            i = 1
            while i < 5:
                self.pixels.fill((0, 255, 0))
                self.pixels.show()
                time.sleep(1)
                print(f'Flashing x{i}')
                self.pixels.fill(0)
                time.sleep(1)
                i += 1
        else:
            # Turn off lights
            print('Turning all pixels off')
            self.pixels.fill(0)

    def update_all_sensors(self):
        self.update_eb_temp()
        self.update_accel_data()
        self.update_location()
        self.update_us_distance()
