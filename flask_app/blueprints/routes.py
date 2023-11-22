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

