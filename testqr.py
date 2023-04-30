from flask import Response
from flask import Flask
from flask import render_template
from imutils.object_detection import non_max_suppression
import imutils
import numpy as np
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
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())


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
    global stream_active
    # loop over frames from the output stream
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            image = imutils.resize(frame, width=min(600, frame.shape[1]))
            orig = image.copy()
            (rects, _) = hog.detectMultiScale(image, winStride=(6, 6), padding=(10, 10), scale=1.15)

            for (x, y, w, h) in rects:
                cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

            if scan_qr_code:
                data, _, _ = detector.detectAndDecode(image)
                if data:
                    print(data)

            _, buffer = cv2.imencode('.jpg', image)
            image = buffer.tobytes()

            stream_active = False
            # yield the output frame in the byte format - hangs here if not actively viewed!!
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   image + b'\r\n')
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
