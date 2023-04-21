import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# RIGHT LA on pins 35 & 36 right
# LEFT LA on pins 37 & 40 left 

right_up = GPIO.setup(35, GPIO.OUT)
right_down = None
left_up = GPIO.setup(40, GPIO.OUT)
left_down = None

# GPIO.setup(36, GPIO.OUT) # ?
# GPIO.setup(37, GPIO.OUT) # ?


def actuators_up(time_seconds: int):
    """
    Moves both linear actuators up for time_seconds.

    :param int time_seconds: The time in seconds the actuators should go up
    """
    GPIO.output(35,GPIO.HIGH)
    GPIO.output(40,GPIO.HIGH)
    print("Actuators going up")
    
    time.sleep(time_seconds)
    GPIO.output(35,GPIO.LOW)
    GPIO.output(40,GPIO.LOW)
    print("Actuators stopping")


