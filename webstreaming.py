from flask import Response
from flask import Flask
from flask import render_template
import random
import time
import cv2


<<<<<<< HEAD
# initialize the video stream and allow the camera sensor to start up
# camera_0 = cv2.VideoCapture(0)  # have to double-check which camera is which


=======
>>>>>>> 01da55d2ae4e35696b564efd36674f2821f9b2ad
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


gstring0 = ' v4l2src device=/dev/video0 ! image/jpeg, format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'
gstring1 = ' v4l2src device=/dev/video1 ! image/jpeg, format=MJPG ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'

# initialize a flask object
app = Flask(__name__)

stream0 = cv2.VideoCapture(gstring0, cv2.CAP_GSTREAMER)
stream1 = cv2.VideoCapture(gstring1, cv2.CAP_GSTREAMER)

time.sleep(2.0)  # give camera time to start up

<<<<<<< HEAD
print('cam1 has image : %s' % stream0.read()[0])  # True = image captured, False = :(
print('cam0 has image : %s' % stream1.read()[0])  # True = image captured, False = :(
=======
print('cam0 has image : %s' % stream0.read()[0])  # True = image captured, False = :(
print('cam1 has image : %s' % stream1.read()[0])
>>>>>>> 01da55d2ae4e35696b564efd36674f2821f9b2ad

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


@app.get("/telemetry")
def telemetry():
    return 'telemetry goes here'


# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)


stream0.release()
stream1.release()
cv2.destroyAllWindows()

