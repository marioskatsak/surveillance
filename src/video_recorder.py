import os
import ffmpeg
from PIL import Image
from audio_recorder import AudioRecorder

class VideoRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.audio_recorder = AudioRecorder()

    def start_recording(self, output_path):
        if not self.is_recording:
            self.video_output_path = output_path
            self.audio_output_path = output_path.replace('.avi', '.wav')
            self.frames = []
            self.audio_recorder.start_recording(self.audio_output_path)
            self.is_recording = True

    def record_frame(self, frame):
        if self.is_recording:
            self.frames.append(frame)

    def stop_recording(self):
        if self.is_recording:
            self.is_recording = False
            self.audio_recorder.stop_recording()
            self.save_video()
            self.combine_audio_video()

    def save_video(self):
        if self.frames:
            self.frames[0].save(self.video_output_path, save_all=True, append_images=self.frames[1:], duration=1000/20, loop=0)

    def combine_audio_video(self):
        video_input = ffmpeg.input(self.video_output_path)
        audio_input = ffmpeg.input(self.audio_output_path)
        output_path = self.video_output_path.replace('.avi', '_with_audio.avi')
        ffmpeg.output(video_input, audio_input, output_path).run(overwrite_output=True)
        os.remove(self.video_output_path)
        os.remove(self.audio_output_path)
        os.rename(output_path, self.video_output_path)