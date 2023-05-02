import time
import cv2
import jetson.inference
import jetson.utils


class CameraStream:

    def __init__(self, video_source_number: int):
        """
        Inits an instance of CameraStream.

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        """
        source_string = f' v4l2src device=/dev/video{video_source_number} io-mode=2 ! image/jpeg ! nvjpegdec ! video/x-raw ! nvvidconv ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'

        self.stream = cv2.VideoCapture(source_string, cv2.CAP_GSTREAMER)
        self.detector = cv2.QRCodeDetector()
        self.scan_qr_code = True  # add logic to turn off/on later (only need at pickup/dropoff)
        self.detect_objects = True  # add logic to turn off/on later (don't need if stationary)
        self.stream_active = False
        self.net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.7)
        self.display = jetson.utils.glDisplay()

        time.sleep(2.0)  # give camera time to start up

        print(f'Video {video_source_number} has image : %s' % self.stream.read()[0])

        if not self.stream.read():
            self.stream.open()
        if not self.stream.isOpened():
            print(f'Cannot open camera {video_source_number}')

    def generate(self):
        """ Loops over frames from the output stream """
        while True:
            success, frame = self.stream.read()  # read the camera frame
            if not success:
                break
            if self.scan_qr_code:
                data, _, _ = self.detector.detectAndDecode(frame)
                if data:
                    print(data)
            if self.detect_objects:
                img, width, height = frame.captureRGBA()
                detections = self.net.Detect(img, width, height)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            # yield the output frame in the byte format
            self.stream_active = False
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   frame + b'\r\n')
            self.stream_active = True

    def object_detect(self):
        """ For object detection while the stream is not active """
        while True:
            time.sleep(0.5)  # check for objects every half second
            if self.stream_active is False:
                pass
