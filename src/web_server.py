from flask import Flask, Response
from camera import Camera
import threading

app = Flask(__name__)
camera = None

def video_feed():
    return Response(camera.get_video_feed(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return "Welcome to the Surveillance System. Access the video feed at /video_feed"

@app.route('/video_feed')
def video_feed_route():
    return video_feed()

def start_web_server(cam):
    global camera
    camera = cam
    thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False))
    thread.start()

if __name__ == '__main__':
    start_web_server(Camera())