from flask import Response
from flask import Flask
from flask import render_template
import threading
import time
import cv2


# initialize flask
app = Flask(__name__)

gstream_source0 = " v4l2src device=/dev/video0 io-mode=2 ! image/jpeg ! nvjpegdec ! video/x-raw ! nvvidconv ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"
gstream_source1 = " v4l2src device=/dev/video1 io-mode=2 ! image/jpeg ! nvjpegdec ! video/x-raw ! nvvidconv ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1"

stream0 = cv2.VideoCapture(gstream_source0, cv2.CAP_GSTREAMER)
stream1 = cv2.VideoCapture(gstream_source1, cv2.CAP_GSTREAMER)

time.sleep(2.0)  # give camera time to start up

print('cam0 has image : %s' % stream0.read()[0])  # True = image captured, False = :(
print('cam1 has image : %s' % stream1.read()[0])

if not stream0.read():
    stream0.open()
if not stream0.isOpened():
    print('Cannot open camera 0')
if not stream1.read():
    stream1.open()
if not stream1.isOpened():
    print('Cannot open camera 1')


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/camera0")
def camera0():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(stream0), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/camera1")
def camera1():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(stream1), mimetype="multipart/x-mixed-replace; boundary=frame")

def run_app():
    app.run(host='0.0.0.0', debug=False)
    stream0.release()
    stream1.release()
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


def generate(camera):
    """ Loops over frames from the output stream """
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # yield the output frame in the byte format
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   frame + b'\r\n')


# check to see if this is the main thread of execution
if __name__ == '__main__':
    server_thread = threading.Thread(target=run_app)
    # telemetry_thread = threading.Thread(target=post_telemetry)
    server_thread.start()
    # telemetry_thread.start()

