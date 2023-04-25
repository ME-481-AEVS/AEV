from flask import Response
from flask import Flask
from flask import render_template
import threading
import time
import cv2

# initialize a flask object
app = Flask(__name__)

camera = cv2.VideoCapture(0)
detector = cv2.QRCodeDetector()

scan_qr_code = True

time.sleep(2.0)

stream_active = False


def qr_code_loop():
    while True:
        time.sleep(1)  # check for qr code every second
        if stream_active is False:
            success, frame = camera.read()
            data, bbox, _ = detector.detectAndDecode(frame)
            if data:
                print(data)


qr_thread = threading.Thread(target=qr_code_loop)
qr_thread.start()


@app.route("/")
def index():
    # return the rendered template
    return render_template("index.html")


def generate():
    # loop over frames from the output stream
    while True:
        time.sleep(0.1)
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            if scan_qr_code:
                data, bbox, _ = detector.detectAndDecode(frame)
                if data:
                    print(data)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            stream_active = False
            # yield the output frame in the byte format - hangs here if not actively viewed!!
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   frame + b'\r\n')
            stream_active = True


@app.route("/camera0")
def camera0():
    # return the response generated along with the specific media
    # type (mime type)
    return Response(generate(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


# check to see if this is the main thread of execution
if __name__ == '__main__':
    app.run(debug=True)


# release the video stream pointer
camera.release()
cv2.destroyAllWindows()
