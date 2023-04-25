import time
import cv2


class CameraStream:

    def __init__(self, video_source_number: int):
        """
        Inits an instance of CameraStream.

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        """
        source_string = f' v4l2src device=/dev/video{video_source_number} io-mode=2 ! image/jpeg ! nvjpegdec ! video/x-raw ! nvvidconv ! videoconvert ! video/x-raw,format=BGR ! appsink drop=1'

        self.stream = cv2.VideoCapture(source_string, cv2.CAP_GSTREAMER)

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
            else:
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                # yield the output frame in the byte format
                yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                       frame + b'\r\n')