import cv2
import os
import json
import threading
import time

from flask import Response, request, jsonify, render_template

from flask_app import app, sock
from aev import AEV
from camera.camera_stream import CameraStream


aev = AEV()


def qr_code_loop():
    """
    To detect a QR code when the stream is not active. Since we are only using one of the cameras
    to check for QR codes, this is defined here instead of in camera_stream.py
    """
    detector = cv2.QRCodeDetector()
    while True:
        time.sleep(1)  # check for qr code every second
        # if camera_rear.stream_active is False:
        #     _, frame = camera_rear.stream.read()
        #     data, _, _ = detector.detectAndDecode(frame)
        #     if data:
        #         if data == 'open sesame':  # todo check for active delivery code
        #             print('QR CODE MATCH - OPENING DOOR')
        #             # open the door
        #         elif data == 'close sesame':
        #             print('QR CODE MATCH - CLOSING DOOR')
        #             # close the door


@sock.route('/telemetry')
def echo(ws):
    data = ws.receive()
    print(data)
    while True:
        aev.update_telemetry()
        ws.send(aev.telemetry)
        print('sending telemetry')
        time.sleep(2)


@sock.route('/control')
def control(ws):
    """
    0000 0000
     ECO WASD
    E: emergency stop   64
    C: close door       32
    O: open door        16
    W: forward           8
    A: left              4
    S: backward          2
    D: right             1
    """
    while ws.connected:
        data = ws.receive()
        data = json.loads(data)
        print(data)
        command = 0
        if data['type'] == 'command':
            command = data['message']
        print(command)
        if command >= 64:
            # emergency stop
            print('EMERGENCY STOP')
        elif command == 32:
            # close door
            print('CLOSING DOOR')
        elif command == 16:
            # open door
            print('OPENING DOOR')
        elif command >= 8:
            # forward
            status = 'MOVING FORWARD'
            if command == 12:
                # left
                status += ' LEFT'
            elif command == 9:
                # right
                status += ' RIGHT'
            else:
                # just forward
                pass
            print(status)
        elif command == 4:
            # left
            print('TURNING LEFT')
        elif command == 1:
            # right
            print('TURNING RIGHT')
        elif command >= 2:
            # backward
            status = 'MOVING BACKWARD'
            if command == 6:
                # left
                status += ' LEFT'
            elif command == 3:
                # right
                status += ' RIGHT'
            else:
                # just back
                pass
            print(status)
        else:
            print('STOPPING')
    print('DISCONNECTED')


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/rear-camera')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/front-camera')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


