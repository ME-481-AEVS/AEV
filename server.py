import cv2
from flask import Response, request, Flask, jsonify, render_template
from flask_cors import CORS
from datetime import datetime
import threading
import time

from linear_actuator_controls import actuators_down, actuators_up
from motor_controls import *
from camera_stream import CameraStream
from env.auth_users import AUTHORIZED_USERS

# initialize flask
app = Flask(__name__)
app.secret_key = 'aev123hehe'
CORS(app)

# manual controls
motor_control = None

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
    else:
        motor_control.exit()
        motor_control = None
        print('Manual control turned off')
    return jsonify(msg='Manual control turned off') if manual == 0 else jsonify(msg='Manual control turned on')

    
@app.post('/command_control')
def command_control():
    global motor_control
    command = int(request.data.decode('UTF-8'))
    if command >= 64:
        # emergency stop
        motor_control.exit()
        motor_control = None
        print('EMERGENCY STOP')
    elif command == 0:
        motor_control.stop()
        print('STOPPING')
    elif command == 8:
        # forward
        # motor_control.forward()
        print('MOVING FORWARD')
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

