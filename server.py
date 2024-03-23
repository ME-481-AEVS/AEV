import cv2
import os
import threading
import time

from flask import Response, request, Flask, jsonify, render_template
from flask_sock import Sock
from flask_cors import CORS
from dotenv import load_dotenv

from aev import AEV


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


@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@app.get('/')
def index():
    return render_template('index.html')


@app.get('/rear-camera')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/front-camera')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.post('/command_center_switch')
def command_center_switch():
    # turns manual controls on/off
    manual = int(request.data.decode('UTF-8'))
    # if manual == 1:
    #     motor_control = MotorControl()
    #     print('Manual control turned on')
    #     heartbeat_thread = threading.Thread(target=check_heartbeat)
    #     heartbeat_thread.start()
    # else:
    #     if motor_control is None:
    #         motor_control = MotorControl()
    #     motor_control.exit()
    #     motor_control = None
    #     print('Manual control turned off')
    return jsonify(msg='Manual control off') if manual == 0 else jsonify(msg='Manual control on')


def run_app():
    # app.run(host='0.0.0.0', debug=False, port=443, ssl_context=('/home/aev/aev/ssl/server.crt', '/home/aev/aev/ssl/server.key'))
    app.run(debug=True)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # qr_thread = threading.Thread(target=qr_code_loop)
    # qr_thread.start()
    run_app()
