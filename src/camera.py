import cv2
import datetime
from picamera2 import Picamera2

class Camera:
    def __init__(self):
        self.picam2 = Picamera2()
        self.picam2.configure(self.picam2.create_preview_configuration(main={"size": (640, 480)}))
        self.picam2.start()

    def get_frame(self):
        frame = self.picam2.capture_array()
        if frame is None:
            return None
        return frame

    def add_timestamp(self, frame):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
        return frame

    def get_video_feed(self):
        while True:
            frame = self.get_frame()
            if frame is None:
                continue
            frame = self.add_timestamp(frame)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

    def release(self):
        self.picam2.stop()