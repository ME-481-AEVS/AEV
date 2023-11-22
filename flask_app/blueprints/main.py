from flask import Blueprint, render_template, Response

main = Blueprint('main', __name__)


@main.get('/')
def index():
    return render_template('index.html')


@main.get('/rear-camera')
def rear():
    return Response(camera_rear.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@main.get('/front-camera')
def front():
    return Response(camera_front.generate(), mimetype='multipart/x-mixed-replace; boundary=frame')
