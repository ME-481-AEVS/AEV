import time
import cv2
import threading
import os

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput

os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"


class CameraStream:

    def __init__(self, video_source_number: int):
        """
        Inits an instance of CameraStream.

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        """
        source_string = f' v4l2src device=/dev/video100 io-mode=2 ! image/jpeg ! nvjpegdec ! video/x-raw ! nvvidconv ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'

        self.input = videoSource("/dev/video0")
        self.output = videoOutput("rtsp://168.105.255.185:5000/camera1")
        self.stream = cv2.VideoCapture("rtsp://168.105.255.185:5000/camera1", cv2.CAP_FFMPEG)
        self.detector = cv2.QRCodeDetector()
        self.scan_qr_code = True  # add logic to turn off/on later (only need at pickup/dropoff)
        self.detect_objects = True  # add logic to turn off/on later (don't need if stationary)
        self.stream_active = False
        self.net = detectNet("ssd-mobilenet-v2", threshold=0.7)

        object_detection_thread = threading.Thread(target=self.obj_detect)
        object_detection_thread.start()

        time.sleep(1)  # give camera time to start up

        print(f'Video {video_source_number} has image : %s' % self.stream.read()[0])

        if not self.stream.read():
            self.stream.open()
        if not self.stream.isOpened():
            print(f'Cannot open camera {video_source_number}')

    def generate(self):
        """ Loops over frames from the output stream """
        if not self.stream.read():
            self.stream.open()
        if not self.stream.isOpened():
            print(f'Cannot open camera')
        while True:
            success, frame = self.stream.read()  # read the camera frame
            if not success:
                break
            if self.scan_qr_code:
                data, _, _ = self.detector.detectAndDecode(frame)
                if data:
                    print(data)
            _, buffer = cv2.imencode('.jpg', frame)

            frame = buffer.tobytes()
            # yield the output frame in the byte format
            self.stream_active = False
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   frame + b'\r\n')
            self.stream_active = True
    
    def obj_detect(self):
        while True:
            img = self.input.Capture()

            if img is None:
                continue

            detections = self.net.Detect(img)

            self.output.Render(img)

