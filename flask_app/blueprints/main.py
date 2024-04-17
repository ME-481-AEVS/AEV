from flask import Blueprint, render_template, Response

from camera.camera_stream import CameraStream


main = Blueprint('main', __name__)


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/rear-camera')
def rear():
    return Response(CameraStream(0).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/front-camera')
def front():
    return Response(CameraStream(1).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/left-camera')
def front():
    return Response(CameraStream(2).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/right-camera')
def front():
    return Response(CameraStream(3).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/misc-camera')
def front():
    return Response(CameraStream(4).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/misc-camera2')
def front():
    return Response(CameraStream(5).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
