# Camera Surveillance System

This project is a camera surveillance system that detects motion, records video and audio, and provides a live video feed accessible via a web browser. The recorded videos are combined into a single file every 24 hours.

## Features

- Motion detection
- Video and audio recording
- Timestamp overlay on video frames
- Live video feed accessible via a web browser
- Combines recorded videos into a single file every 24 hours

## Prerequisites

- Python 3.x
- Raspberry Pi with Raspbian OS (or any other Linux-based system)
- Raspberry Pi Camera Module 3
- Microphone for audio recording

### Install Dependencies

1. Update and upgrade the system:
    ```bash
    sudo apt-get update
    sudo apt-get upgrade
    ```

2. Enable the camera interface:
    ```bash
    sudo raspi-config
    ```
    - Navigate to `Interfacing Options`.
    - Select `Camera` and enable it.
    - Reboot the Raspberry Pi.

3. Install `picamera2`:
    ```bash
    sudo apt-get install -y python3-picamera2
    ```

4. Install `Pillow`:
    ```bash
    pip install pillow
    ```

5. Install the necessary development libraries for `pyaudio`:
    ```bash
    sudo apt-get install portaudio19-dev
    ```

6. Install `pyaudio` and `ffmpeg-python`:
    ```bash
    pip install pyaudio ffmpeg-python
    ```

7. Install `ffmpeg`:
    ```bash
    sudo apt-get install ffmpeg
    ```

### Clone the Repository

```bash
git clone https://github.com/yourusername/camera_surveillance.git
cd camera_surveillance/src