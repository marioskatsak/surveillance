import numpy as np

class MotionDetector:
    def __init__(self):
        self.previous_frame = None

    def detect_motion(self, frame):
        gray = np.dot(frame[...,:3], [0.2989, 0.5870, 0.1140])
        gray = gray.astype(np.uint8)

        if self.previous_frame is None:
            self.previous_frame = gray
            return False

        frame_delta = np.abs(self.previous_frame - gray)
        thresh = np.where(frame_delta > 25, 255, 0).astype(np.uint8)
        self.previous_frame = gray

        if np.sum(thresh) > 500:
            return True

        return False