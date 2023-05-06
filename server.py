import cv2
import threading
import time
import RPi.GPIO as GPIO
import urllib.request

from flask import Response, request, Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime

from controls.linear_actuator_controls import actuators_down, actuators_up
from controls.motor_controls import *
from camera.camera_stream import CameraStream
from env.auth_users import AUTHORIZED_USERS
from telemetry import Telemetry


# initialize flask
app = Flask(__name__)
app.secret_key = 'aev123hehe'
CORS(app)

# telemetry
telemetry_data = {}
current_speed = 0
door_status = 'c'

# manual controls
motor_control = None
heartbeat_int = 0

"""
def e_stop():
    print('E-STOP BUTTON STATE CHANGE')
    if GPIO.output(12, 1):
        print('Button pressed, stopping')
    else:
        print('Button unpressed, resuming normal operation')


def sensor_press():
    print('TACTILE BUTTON STATE CHANGE')
    if GPIO.output(13, 1):
        print('Button pressed, we\'ve been hit!')
    else:
        print('Button unpressed')
"""

def qr_code_loop():
    """
    To detect a QR code when the stream is not active. Since we are only using one of the cameras
    to check for QR codes, this is defined here instead of in camera_stream.py
    """
    global camera_rear
    global door_status
    detector = cv2.QRCodeDetector()
    while True:
        time.sleep(1)  # check for qr code every second
        if camera_rear.stream_active is False:
            _, frame = camera_rear.stream.read()
            data, _, _ = detector.detectAndDecode(frame)
            if data:
                if data == 'open sesame':
                    print('QR CODE MATCH - OPENING DOOR')
                    actuators_up(12)
                    time.sleep(12)
                    door_status = 'o'
                elif data == 'close sesame':
                    print('QR CODE MATCH - CLOSING DOOR')
                    actuators_down(12)
                    time.sleep(12)
                    door_status = 'c'


@app.route('/')
def index():
    # return the rendered template
    return render_template('index.html')


@app.route('/rear')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/front')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.post('/command_center_switch')
def command_center_switch():
    global motor_control
    # turns manual controls on/off
    manual = int(request.data.decode('UTF-8'))
    if manual == 1:
        motor_control = MotorControl()
        print('Manual control turned on')
        heartbeat_thread = threading.Thread(target=check_heartbeat)
        heartbeat_thread.start()
    else:
        if motor_control is None:
            motor_control = MotorControl()
        motor_control.exit()
        motor_control = None
        print('Manual control turned off')
    return jsonify(msg='Manual control off') if manual == 0 else jsonify(msg='Manual control on')


@app.post('/heartbeat')
def heartbeat():
    global heartbeat_int
    global motor_control
    heartbeat_int = int(request.data.decode('UTF-8'))
    return jsonify(motorcontrols=True if motor_control else False)


@app.post('/command_control')
def command_control():
    global motor_control
    global current_speed
    global door_status
    command = int(request.data.decode('UTF-8'))

    '''
    0000 0000
     ECO WASD
    E: emergency stop   64
    C: close door       32
    O: open door        16
    W: forward           8
    A: left              4
    S: backward          2
    D: right             1
    '''
    if command >= 64:
        # emergency stop
        if not motor_control:
            motor_control = MotorControl()
        motor_control.exit()
        motor_control = None
        print('EMERGENCY STOP')
        current_speed = 0
    elif command == 32:
        # open door
        print('OPENING DOOR')
        actuators_up(12)
        time.sleep(12)
        door_status = 'o'
    elif command == 16:
        # close door
        print('CLOSING DOOR')
        actuators_down(12)
        time.sleep(12)
        door_status = 'c'
    elif command >= 8:
        # forward
        status = 'MOVING FORWARD'
        if command == 12:
            # left
            motor_control.foward_left()
            status += ' LEFT'
            current_speed = 2
        elif command == 9:
            # right
            motor_control.foward_right()
            status += ' RIGHT'
            current_speed = 2
        else:
            motor_control.forward()
            current_speed = 3
        print(status)
    elif command == 4:
        # left
        motor_control.left()
        print('TURNING LEFT')
    elif command == 1:
        # right
        motor_control.right()
        print('TURNING RIGHT')
    elif command >= 2:
        # backward
        status = 'MOVING BACKWARD'
        if command == 6:
            # left
            motor_control.reverse_left()
            status += ' LEFT'
            current_speed = 2
        elif command == 3:
            # right
            motor_control.reverse_right()
            status += ' RIGHT'
            current_speed = 2
        else:
            motor_control.reverse()
            current_speed = 3
        print(status)
    else:
        motor_control.stop()
        print('STOPPING')
        current_speed = 0
    return jsonify(msg=command)


# todo rename to user_control (will need to update user website as well
@app.post('/control')
def control():
    global door_status
    command = request.values.get('command')
    name = request.values.get('user')
    if name in AUTHORIZED_USERS:
        with open('log/control.log', 'a') as file:
            file.write(f'%-22s%-12s%-s\n' % (name, command, datetime.now()))
        if command == 'open':
            print('RECEIVED REMOTE COMMAND - OPENING DOOR')
            actuators_up(12)
            time.sleep(12)
            door_status = 'o'
        elif command == 'close':
            print('RECEIVED REMOTE COMMAND - CLOSING DOOR')
            actuators_down(12)
            time.sleep(12)
            door_status = 'c'
        else:
            print('RECEIVED UNRECOGNIZED REMOTE COMMAND')
    else:
        with open('log/control.log', 'a') as file:
            file.write('UNAUTHORIZED USER:\n')
            file.write(f'%-22s%-12s%-s\tACCESS DENIED\n' % (name, command, datetime.now()))
        
    return {'command': command}


@app.get('/telemetry')
def telemetry():
    return telemetry_data


def check_heartbeat():
    global heartbeat_int
    global motor_control
    local_heartbeat = 0
    heartbeat_int = 0
    while motor_control:
        time.sleep(1)
        if local_heartbeat > heartbeat_int:
            print('Lost contact with control center, turning off motor controls')
            if motor_control is None:
                motor_control = MotorControl()
            motor_control.exit()
            motor_control = None
            break
        local_heartbeat += 1


def update_telemetry():
    global telemetry_data
    global door_status
    global current_speed
    tele = Telemetry()

    while True:
        external_ip = urllib.request.urlopen('https://v4.ident.me/').read().decode('utf8')

        tele.update_all_sensors()
        tele.print_telemetry()
        telemetry_data = {
            "status": 1,
            "currentOrderId": None,
            "ipAddress": external_ip,
            "batteryLevel": 82,
            "state": 1,
            "door": door_status,
            "speed": current_speed,
            "accelerometer": tele.accel_data,
            "lat": tele.lat,
            "long": tele.long,
            "boltLock": True,
            "brakes": True,
            "cpuTemp": 53.5,
            "elecBayTemp": tele.eb_temp,
        }
        time.sleep(2)


def run_app():
    app.run(host='0.0.0.0', debug=False, port=443, ssl_context=('/home/aev/aev/ssl/server.crt', '/home/aev/aev/ssl/server.key'))
    if motor_control:
        motor_control.exit()
    rear_stream.release()
    cv2.destroyAllWindows()


# check to see if this is the main thread of execution
if __name__ == '__main__':
    qr_thread = threading.Thread(target=qr_code_loop)
    server_thread = threading.Thread(target=run_app)
    telemetry_thread = threading.Thread(target=update_telemetry)

    # camera streams
    camera_rear = CameraStream(0)
    camera_front = CameraStream(1)
    #camera_front2 = ODCameraStream(2, 'front2')

    telemetry_thread.start()
    qr_thread.start()
    server_thread.start()

    GPIO.setmode(GPIO.BOARD)
    print(f'\n\n\nGPIO MODE: {GPIO.getmode()}\n\n\n')
