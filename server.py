import cv2
from flask import Response, request, Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import threading

from linear_actuator_controls import actuators_down, actuators_up
from motor_controls import *
from camera_stream import CameraStream
from env.auth_users import AUTHORIZED_USERS
from sensors import *


# initialize flask
app = Flask(__name__)
app.secret_key = 'aev123hehe'
CORS(app)

# manual controls
motor_control = None
heartbeat_int = 0

# camera streams
cam0 = CameraStream(0)
cam1 = CameraStream(1)


@app.route('/')
def index():
    # return the rendered template
    return render_template('index.html')


@app.route('/camera0')
def camera0():
    return Response(cam0.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera1')
def camera1():
    return Response(cam1.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


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
        motor_control.exit()
        motor_control = None
        print('Manual control turned off')
    return jsonify(msg='Manual control turned off') if manual == 0 else jsonify(msg='Manual control turned on')


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


def run_app():
    app.run(host='0.0.0.0', debug=False)
    if motor_control:
        motor_control.exit()
    cam0.stream.release()
    cam1.stream.release()
    cv2.destroyAllWindows()


def check_heartbeat():
    global heartbeat_int
    global motor_control
    local_heartbeat = heartbeat_int
    while motor_control:
        time.sleep(1)
        if local_heartbeat >= heartbeat_int:
            motor_control.exit()
            motor_control = None
            break
        local_heartbeat += 1


def post_telemetry():
    while True:
        time.sleep(2)
        telemetry = {
            "status": 1,
            "currentOrderId": None,
            "ipAddress": "0.0.0.0",
            "batteryLevel": 69,
            "state": 1,
            "speed": 2.4,
            "accelerometer": "1.2, 2.1, 2.8",
            "boltLock": True,
            "brakes": True,
            "cpuTemp": 53.5,
            "elecBayTemp": 58.1,
            "gps": 3
        }
        # res = requests.post('http://localhost:3000/robot/aev1', json=telemetry)
        # print('response from server:', res.text)


# check to see if this is the main thread of execution
if __name__ == '__main__':
    server_thread = threading.Thread(target=run_app)
    # telemetry_thread = threading.Thread(target=post_telemetry)
    server_thread.start()
    # telemetry_thread.start()

