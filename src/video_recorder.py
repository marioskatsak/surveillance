import cv2
import ffmpeg
import os
from audio_recorder import AudioRecorder

class VideoRecorder:
    def __init__(self):
        self.is_recording = False
        self.video_writer = None
        self.audio_recorder = AudioRecorder()

    def start_recording(self, output_path):
        if not self.is_recording:
            self.video_output_path = output_path
            self.audio_output_path = output_path.replace('.avi', '.wav')

            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(self.video_output_path, fourcc, 20.0, (640, 480))
            self.audio_recorder.start_recording(self.audio_output_path)
            self.is_recording = True

    def record_frame(self, frame):
        if self.is_recording:
            self.video_writer.write(frame)

    def stop_recording(self):
        if self.is_recording:
            self.video_writer.release()
            self.audio_recorder.stop_recording()
            self.is_recording = False
            self.combine_audio_video()

    def combine_audio_video(self):
        video_input = ffmpeg.input(self.video_output_path)
        audio_input = ffmpeg.input(self.audio_output_path)
        output_path = self.video_output_path.replace('.avi', '_with_audio.avi')
        ffmpeg.output(video_input, audio_input, output_path).run(overwrite_output=True)
        os.remove(self.video_output_path)
        os.remove(self.audio_output_path)
        os.rename(output_path, self.video_output_path)