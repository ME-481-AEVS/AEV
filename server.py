import cv2
import os
import threading
import time

from flask import Response, request, Flask, jsonify, render_template
from flask_sock import Sock
from flask_cors import CORS
from dotenv import load_dotenv

from aev import AEV
from camera.camera_stream import CameraStream


# initialize flask
load_dotenv()
app = Flask(__name__)
app.config['SOCK_SERVER_OPTIONS'] = {'ping_interval': 25}
app.secret_key = os.environ.get('FLASK_SECRET_KEY')
sock = Sock(app)
CORS(app)
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
        time.sleep(1)


@sock.route('/control')
def control(ws):
    data = ws.receive()
    print(data)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/rear-camera')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/front-camera')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


def run_app():
    # app.run(host='0.0.0.0', debug=False, port=443, ssl_context=('/home/aev/aev/ssl/server.crt', '/home/aev/aev/ssl/server.key'))
    app.run(debug=True, host='0.0.0.0')
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # qr_thread = threading.Thread(target=qr_code_loop)
    # qr_thread.start()

    camera_rear = CameraStream(0)
    run_app()
