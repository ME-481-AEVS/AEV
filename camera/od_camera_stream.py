import time
import cv2
import threading
import os

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput


class ODCameraStream:
    """ Camera stream with object detection capability """

    def __init__(self, video_source_number: int, position: str):
        """
        Inits an instance of CameraStream

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        :param str position: The position of the camera - e.g. 'front1', 'front2', 'rear'
        """
        self.input = videoSource(f'/dev/video{video_source_number}')
        self.output = videoOutput(f'webrtc://@:8554/{position}')
        self.detect_objects = True  # add logic to turn off/on later (don't need if stationary)
        self.net = detectNet("ssd-mobilenet-v2", threshold=0.7)

        object_detection_thread = threading.Thread(target=self.obj_detect)
        object_detection_thread.start()

    def obj_detect(self):
        """
        Controls object detection and outputs stream
        """
        while True:
            img = self.input.Capture()

            if img is None:
                print('Object detection camera stream: No image')
                continue

            detections = self.net.Detect(img)

            self.output.Render(img)

