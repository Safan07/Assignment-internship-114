# Face Blurring & Video Recording Application

## Overview
This Python application captures a **live video feed** from a webcam, **detects faces**, and applies **pixelation and/or Gaussian blur** to anonymize them. It also allows the user to **record the processed video** and save snapshots. The GUI is built with **Tkinter** for easy control of camera, blur, and recording functions.

---

## Features

- **Live webcam feed** display.
- **Face detection** using OpenCV Haar Cascades.
- **Blurred faces** (pixelation + Gaussian blur) to anonymize identities.
- **Toggle blur** ON/OFF in real-time.
- **Video recording** of processed feed.
- **Snapshot capture** of current frame.
- **Real-time FPS display**.
- **Clean Tkinter GUI** for controls.
- **Graceful exit**: stops camera and recording on app close.

---

## Requirements

- Python 3.8+
- OpenCV (`opencv-python`)
- Pillow (`PIL`)
- Tkinter (built-in)
- Numpy

Install dependencies:

```bash
pip install opencv-python Pillow numpy
Usage
Run the application:

bash
Copy code
python face_blur_app.py
GUI Controls:

Button	Description
Open Camera	Start webcam feed
Close Camera	Stop webcam feed
Blur ON/OFF	Toggle face blur
Start/Stop Recording	Record processed video
Snapshot	Take a snapshot of current frame

Keyboard Shortcuts:

Press q to close the app safely.

Recorded Videos:

Videos are saved in the recordings/ folder with timestamped filenames.

Snapshots are saved in the snapshots/ folder.

File Structure
bash
Copy code
project/
│
├─ face_blur_app.py      # Main Python script
├─ recordings/           # Saved video recordings
├─ snapshots/            # Saved snapshots
└─ haarcascade_frontalface_default.xml  # Haar cascade model
Notes
Ensure the camera is not used by another application before starting.

Adjust scaleFactor and minNeighbors in the Haar cascade for better detection accuracy.

The blur effect can be adjusted by changing the Gaussian kernel size in the code.

License
This project is open-source and free to use for educational purposes.

yaml
Copy code
