import pyaudio
import wave
import threading

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.stream = None
        self.p = pyaudio.PyAudio()

    def start_recording(self, output_path):
        self.is_recording = True
        self.output_path = output_path
        self.frames = []

        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)

        self.thread = threading.Thread(target=self.record)
        self.thread.start()

    def record(self):
        while self.is_recording:
            data = self.stream.read(1024)
            self.frames.append(data)

    def stop_recording(self):
        self.is_recording = False
        self.thread.join()

        self.stream.stop_stream()
        self.stream.close()

        wf = wave.open(self.output_path, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(self.p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b''.join(self.frames))
        wf.close()

    def terminate(self):
        self.p.terminate()