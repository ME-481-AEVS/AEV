import cv2
from flask import Response, request, Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import threading
import time
import socket

from controls.linear_actuator_controls import actuators_down, actuators_up
from controls.motor_controls import *
from camera_stream import CameraStream
from env.auth_users import AUTHORIZED_USERS

from telemetry import Telemetry


# initialize flask
app = Flask(__name__)
app.secret_key = 'aev123hehe'
CORS(app)

# telemetry
telemetry_data = {}

# manual controls
motor_control = None
heartbeat_int = 0


def qr_code_loop():
    """
    To detect a QR code when the stream is not active. Since we are only using one of the cameras
    to check for QR codes, this is defined here instead of in camera_stream.py
    
    TODO not updated to account for new streaming method
    """
    global cam0
    detector = cv2.QRCodeDetector()
    while True:
        time.sleep(1)  # check for qr code every second
        if cam0.stream_active is False:
            _, frame = cam0.stream.read()
            data, _, _ = detector.detectAndDecode(frame)
            if data:
                print(data)


@app.route('/')
def index():
    # return the rendered template
    return render_template('index.html')


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
    elif command == 32:
        # open door
        print('OPENING DOOR')
        # actuators_up(12)
    elif command == 16:
        # close door
        print('CLOSING DOOR')
        # actuators_down(12)
    elif command >= 8:
        # forward
        status = 'MOVING FORWARD'
        if command == 12:
            # left
            # motor_control.foward_left()
            status += ' LEFT'
        elif command == 9:
            # right
            # motor_control.foward_right()
            status += ' RIGHT'
        else:
            motor_control.forward()
        print(status)
    elif command == 4:
        # left
        # motor_control.left()
        print('TURNING LEFT')
    elif command == 1:
        # right
        # motor_control.right()
        print('TURNING RIGHT')
    elif command >= 2:
        # backward
        status = 'MOVING BACKWARD'
        if command == 6:
            # left
            # motor_control.reverse_left()
            status += ' LEFT'
        elif command == 3:
            # right
            # motor_control.reverse_right()
            status += ' RIGHT'
        else:
            motor_control.reverse()
        print(status)
    else:
        motor_control.stop()
        print('STOPPING')
    return jsonify(msg=command)


# todo rename to user_control (will need to update user website as well
@app.post('/control')
def control():
    command = request.values.get('command')
    name = request.values.get('user')
    if name in AUTHORIZED_USERS:
        with open('log/control.log', 'a') as file:
            file.write(f'%-22s%-12s%-s\n' % (name, command, datetime.now()))
        if command == 'open':
            print('RECEIVED REMOTE COMMAND - OPENING DOOR')
            actuators_up(12)
        elif command == 'close':
            print('RECEIVED REMOTE COMMAND - CLOSING DOOR')
            actuators_down(12)
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


def run_app():
    app.run(host='0.0.0.0', debug=False)
    if motor_control:
        motor_control.exit()


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
    tele = Telemetry()

    while True:
        tele.update_all_sensors()
        tele.print_telemetry()
        telemetry_data = {
            "status": 1,
            "currentOrderId": None,
            "ipAddress": socket.gethostbyname(socket.gethostname()),
            "batteryLevel": 69,
            "state": 1,
            "speed": 2.4,
            "accelerometer": tele.accel_data,
            "lat": tele.lat,
            "long": tele.long,
            "boltLock": True,
            "brakes": True,
            "cpuTemp": 53.5,
            "elecBayTemp": tele.eb_temp,
        }
        time.sleep(2)


# check to see if this is the main thread of execution
if __name__ == '__main__':
    qr_thread = threading.Thread(target=qr_code_loop)
    server_thread = threading.Thread(target=run_app)
    telemetry_thread = threading.Thread(target=update_telemetry)
    telemetry_thread.start()
    server_thread.start()

    # camera streams
    camera_back = CameraStream(0, 'back')

