from flask import Blueprint, render_template, Response

from camera.camera_stream import CameraStream


main = Blueprint('main', __name__)
camera_rear = CameraStream(0)


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/rear-camera')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/front-camera')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
