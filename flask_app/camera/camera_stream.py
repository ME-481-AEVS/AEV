import cv2

class CameraStream:
    def __init__(self, video_source_number: int):
        """
        Inits an instance of CameraStream.

        :param int video_source_number: The video resource (e.g. to use /dev/video0, video_source_number = 0)
        """
        self.stream = cv2.VideoCapture(video_source_number)
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
