import RPi.GPIO as GPIO
import vlc
import time

"""
Pins:
  29: Down right
  33: Down left
  35: Up left
  40: Up right
"""


def actuators_up(time_seconds: int):
    """
    Moves both linear actuators up (pins 35 & 40) for time_seconds.
    :param int time_seconds: The time in seconds the actuators should go up
    """
    msg = vlc.MediaPlayer('media/audio/door_opening.mp3')

    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)

    GPIO.output(35, GPIO.HIGH)
    GPIO.output(40, GPIO.HIGH)

    print("Actuators going up")
    msg.play()
    time.sleep(time_seconds)

    GPIO.output(35, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)

    print("Actuators stopping")
    GPIO.cleanup()


def actuators_down(time_seconds: int):
    """
    Moves both linear actuators down (pins 29 and 33) for time_seconds.
    :param int time_seconds: The time in seconds the actuators should go down
    """
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)

    GPIO.output(29, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)

    print("Actuators going down")
    # playsound('media/audio/Door Closing.mp3')
    time.sleep(time_seconds)
    
    GPIO.output(29, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)

    print("Actuators stopping")
    GPIO.cleanup()


def test_pin(pin_number):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin_number, GPIO.OUT)
    GPIO.output(pin_number, GPIO.HIGH)
    stop = input('Press enter to stop')
    GPIO.output(pin_number, GPIO.LOW)
    GPIO.cleanup()


def test_up():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(40, GPIO.HIGH)
    stop = input('Press enter to stop')
    GPIO.output(35, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)
    GPIO.cleanup()


def test_down():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(33, GPIO.OUT)
    GPIO.output(29, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    stop = input('Press enter to stop')
    GPIO.output(29, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.cleanup()
