import cv2
from camera import Camera
from motion_detector import MotionDetector
from video_recorder import VideoRecorder
from web_server import start_web_server
import datetime
import os
import time
import glob
import ffmpeg

def add_timestamp(frame):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, timestamp, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1, cv2.LINE_AA)
    return frame

def combine_videos():
    date = datetime.datetime.now().strftime("%Y%m%d")
    output_path = f"recorded_videos/{date}_combined.mp4"
    video_files = sorted(glob.glob("recorded_videos/motion_*.avi"))

    if not video_files:
        return

    # Create a text file with the list of video files to be combined
    with open("video_list.txt", "w") as f:
        for video_file in video_files:
            f.write(f"file '{os.path.abspath(video_file)}'\n")

    # Use ffmpeg to combine and compress the videos
    ffmpeg.input("video_list.txt", format="concat", safe=0).output(
        output_path, vcodec="libx264", crf=23, preset="medium"
    ).run(overwrite_output=True)

    # Remove the individual video files and the list file
    for video_file in video_files:
        os.remove(video_file)
    os.remove("video_list.txt")

def main():
    camera = Camera()
    motion_detector = MotionDetector()
    video_recorder = VideoRecorder()

    # Ensure the directory for recorded videos exists
    os.makedirs("recorded_videos", exist_ok=True)

    # Start the web server in a separate thread
    start_web_server(camera)

    last_motion_time = None
    recording_started = False
    last_combination_time = time.time()

    while True:
        frame = camera.get_frame()
        if frame is None:
            continue

        frame = add_timestamp(frame)

        if motion_detector.detect_motion(frame):
            last_motion_time = time.time()
            if not recording_started:
                date_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                output_path = f"recorded_videos/motion_{date_time}.avi"
                video_recorder.start_recording(output_path)
                recording_started = True
            video_recorder.record_frame(frame)
        else:
            if recording_started and (time.time() - last_motion_time) >= 5:
                video_recorder.stop_recording()
                recording_started = False

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Combine videos every 24 hours
        # if time.time() - last_combination_time >= 86400:
        if time.time() - last_combination_time >= 120:
            combine_videos()
            last_combination_time = time.time()

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()