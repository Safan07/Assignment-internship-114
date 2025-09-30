# Face Feature Detection - Multi-Face

This project is a **real-time face detection and feature localization application** using Python, OpenCV, MediaPipe, and Tkinter. It detects multiple faces in a video stream, identifies key facial features (nose, eyes, mouth), and annotates them visually. The application also provides options to record video and take snapshots.

---

## Features

- **Multi-face detection** using MediaPipe Face Detection.
- **Facial landmark detection** using MediaPipe Face Mesh:
  - Nose tip
  - Left and right eyes
  - Mouth center
- **Annotations** on video frames with bounding boxes and labels.
- **Video recording** functionality.
- **Snapshot capturing**.
- **Real-time GUI** built with Tkinter, featuring:
  - Dark theme
  - Camera control buttons
  - Status bar updates

---

## Computer Vision Problem

This project addresses a **Face Detection and Facial Landmark Localization** problem:

- **Face Detection:** Locates faces in an image or video frame.
- **Facial Landmark Localization:** Identifies specific points on the face, such as eyes, nose tip, and mouth.  
- **Justification:** This is a **computer vision problem** because it involves interpreting pixel data to detect and understand faces, a classic task in image analysis and human-computer interaction.

---

## Requirements

- Python 3.8+
- OpenCV
- MediaPipe
- Pillow
- Tkinter (usually included with Python)

Install dependencies using:

```bash
pip install opencv-python mediapipe pillow
Usage
Run the application:

bash
Copy code
python your_script_name.py
Controls:

Open Camera: Starts the webcam feed.

Close Camera: Stops the webcam feed.

Start/Stop Recording: Records the live video to output.avi.

Take Snapshot: Saves a frame from the video in the snapshots/ folder.

Press q or Q to close the application.

Output:

Annotated video frames with detected faces and landmarks.

Snapshots saved in snapshots/ folder.

Recorded videos saved as output.avi.

Folder Structure
bash
Copy code
project/
│
├── snapshots/           # Saved snapshots
├── output.avi           # Recorded video
├── face_detection.py    # Main application script
└── README.md            # Project documentation
Notes
The application uses MediaPipe Face Mesh for high-precision landmark detection.

Supports multiple faces simultaneously.

GUI is optimized for a dark theme and responsive design.

Author
Safan Ur Rahman
Internship Project - Face Detection & Feature Localization