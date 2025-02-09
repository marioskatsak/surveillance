from picamera2 import Picamera2
from PIL import Image, ImageDraw, ImageFont
import datetime
import io

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
        image = Image.fromarray(frame)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        draw.text((10, frame.shape[0] - 20), timestamp, font=font, fill=(0, 255, 0))
        return image

    def get_video_feed(self):
        while True:
            frame = self.get_frame()
            if frame is None:
                continue
            frame = self.add_timestamp(frame)
            with io.BytesIO() as output:
                frame.save(output, format="JPEG")
                frame_bytes = output.getvalue()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    def release(self):
        self.picam2.stop()