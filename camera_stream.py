import time
import cv2
import threading
import os

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput


class CameraStream:

    def __init__(self, video_source_number: int, position: str):
        """
        Inits an instance of CameraStream

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        :param str position: The position of the camera - must be 'front', 'back', 'left', or 'right')
        """
        self.input = videoSource(f'/dev/video{video_source_number}')
        self.output = videoOutput(f'webrtc://@:8554/{position}')
        self.detector = cv2.QRCodeDetector()
        self.scan_qr_code = True  # add logic to turn off/on later (only need at pickup/dropoff)
        self.detect_objects = True  # add logic to turn off/on later (don't need if stationary)
        # self.stream_active = False
        self.net = detectNet("ssd-mobilenet-v2", threshold=0.7)

        object_detection_thread = threading.Thread(target=self.obj_detect)
        object_detection_thread.start()

        time.sleep(1)  # give camera time to start up

    def obj_detect(self):
        """
        Controls object detection and outputs stream

        TODO make separate function for qr code, implement logic to turn on/off object detection and 
        qr code detection - also figure out qr code detection for new streaming method
        """
        while True:
            img = self.input.Capture()

            if img is None:
                print('no image :(')
                continue

            #if self.scan_qr_code:
            #    data, _, _ = self.detector.detectAndDecode(img)
            #    if data:
            #        print(data)

            detections = self.net.Detect(img)

            self.output.Render(img)

