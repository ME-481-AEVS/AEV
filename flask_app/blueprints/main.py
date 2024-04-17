from flask import Blueprint, render_template, Response

from camera.camera_stream import CameraStream


main = Blueprint('main', __name__)


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/rear-camera')
def rear_camera():
    return Response(CameraStream(0).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/front-camera')
def front_camera():
    return Response(CameraStream(1).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/left-camera')
def left_camera():
    return Response(CameraStream(2).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/right-camera')
def right_camera():
    return Response(CameraStream(3).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/misc-camera')
def misc_camera():
    return Response(CameraStream(4).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/misc-camera2')
def misc_camera_2():
    return Response(CameraStream(5).generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
