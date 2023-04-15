# AEV sensor data collection functions

# author: Owen Bramley
# date modified: 04/10/2023
# version: 0.1 (alpha)


import time
import board
import neopixel_spi as neopixel
import adafruit_ahtx0
import adafruit_adxl34x

# configure neopixel pins
pixels = neopixel.NeoPixel_SPI(board.SPI(), 30)


# EB_temp
# type: float
# return: temperature reading from the AHT20 board
def EB_temp():
    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_ahtx0.AHTx0(i2c)

    # return the current temperaturre of the EB Bay
    return sensor.temperature


# accel_data()
# type: array
# return: accelerometer readings (yaw, roll, pitch)
def accel_data():
    # initilize I2C connection with the ADXL345 board
    i2c = board.I2C()
    accelerometer = adafruit_adxl34x.ADXL345(i2c)

    # print the accelerometer readings
    print("%f %f %f" % accelerometer.acceleration)
    time.sleep(0.2)

    return accelerometer.acceleration


# get_coorodinates()
# type: array
# return: current coordinatess
def get_corr():
    return


# US_distance(*sensor number*)
# type: boolean
# return: if an object is detected within 1 foot = true else = false
def US_distance(sensor_id):
    # threashold for object detection
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


def lights(state: int):
    """
    Changes the state of the neopixel warning lights.

    :param int state: The new state of the warning lights:
        0: off
        1: solid
        2: Flashing
    """
    match state:
        case 1:
            # Fill all pixels yellow
            print('Turning all pixels on, solid yellow')
            pixels.fill((0, 255, 0))
            pixels.show()
        case 2:
            # Flash lights
            print('Flashing pixels five times, solid yellow')
            pixels.fill((0, 255, 0))

            i = 1
            while i < 5:
                pixels.fill((0, 255, 0))
                pixels.show()
                time.sleep(1)
                print(f'Flashing x{i}')
                pixels.fill((0, 0, 0))
                time.sleep(1)
                i += 1
        case _:
            # Turn off lights
            print('Turning all pixels off')
            pixels.fill((0, 0, 0))


# a function to fetch all sensor data
def get_a_sensors():
    return
