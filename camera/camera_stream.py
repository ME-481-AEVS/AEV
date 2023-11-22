import cv2

class CameraStream:
    def __init__(self, video_source_number: int):
        """
        Inits an instance of CameraStream.

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        """
        # 3d camera res 2560x960
        source_string = 'v4l2src device=/dev/video0 io-mode=2 ! image/jpeg,format=MJPG,width=2560,height=960,framerate=30/1 ! nvv4l2decoder mjpeg=1 ! nvvidconv ! video/x-raw,format=BGRx ! appsink drop=1'
        source_string = 'v4l2src device=/dev/video0 io-mode=2 ! video/x-raw,format=MJPG,width=2560,height=960,framerate=30/1 ! nvvidconv ! video/x-raw(memory:NVMM) ! nvvidconv ! video/x-raw, format=BGRx ! appsink drop=1'
        source_string = 'nvarguscamerasrc ! video/x-raw(memory:NVMM),format=NV12,width=2560,height=960,framerate=30/1 ! nvvidconv ! video/x-raw,format=BGRx ! appsink drop=1'
        print(source_string)
        #self.stream = cv2.VideoCapture(source_string, cv2.CAP_GSTREAMER)
        self.stream = cv2.VideoCapture("/dev/video0")
        # self.stream = cv2.VideoCapture(video_source_number)
        if not self.stream.isOpened():
            print(f'Cannot open camera {video_source_number}')

    def generate(self):
        """ Loops over frames from the output stream """
        try:
            while True:
                success, frame = self.stream.read()  # read the camera frame
                if not success:
                    break

                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()

                # yield the output frame in the byte format
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' +
                       frame + b'\r\n')
        finally:
            self.__del__()

    def __del__(self):
        """
        Releases the camera stream when the object is destroyed
        """
        if self.stream.isOpened():
            self.stream.release()
