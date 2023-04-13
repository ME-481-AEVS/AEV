from flask import Response
from flask import Flask
from flask import render_template
import random
import time
import cv2


# initialize the video stream and allow the camera sensor to start up
# camera_0 = cv2.VideoCapture(0)  # have to double-check which camera is which


def __gstreamer_pipeline(camera_id, capture_width=1280, capture_height=720, display_width=1280, display_height=720, framerate=30, flip_method=0):
    return (
            "nvarguscamerasrc sensor-id=%d ! video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, format=(string)NV12, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink max-buffers=1 drop=True"
            % (camera_id, capture_width, capture_height, framerate, flip_method, display_width, display_height)
    )


def generate(camera):
    """ Loop over frames from the output stream """
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


# initialize a flask object
app = Flask(__name__)

stream = cv2.VideoCapture(0)

time.sleep(2.0)  # give camera time to start up

print('cam has image : %s' % stream.read()[0])  # True = image captured, False = :(

if not stream.read():
    stream.open()
if not stream.isOpened():
    print('Cannot open camera')


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


@app.route("/camera0")
def camera0():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(stream), mimetype="multipart/x-mixed-replace; boundary=frame")


"""
@app.route("/camera1")
def camera1():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(camera_1), mimetype="multipart/x-mixed-replace; boundary=frame")

@app.route("/camera2")
def camera2():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(camera_2), mimetype="multipart/x-mixed-replace; boundary=frame")
"""


@app.get("/telemetry")
def telemetry():
    print(random.random())
    return str(random.random())


# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
