import cv2
import mediapipe as mp
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import datetime
import os

# --- MediaPipe Models ---
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

face_detection = mp_face_detection.FaceDetection(min_detection_confidence=0.5)
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=5, refine_landmarks=True)

# --- Globals ---
cap = None
recording = False
out = None

# --- Dark Style ---
class DarkStyle(ttk.Style):
    def __init__(self, root):
        super().__init__(root)
        self.theme_use('clam')
        self.configure('.', background='#1c1c2e', foreground='white', font=('Arial', 10))
        self.map('TButton', foreground=[('active', 'white')], background=[('active', '#0055ff')])

# --- Functions ---
def start_camera():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        update_frame()
        status_bar.config(text="Camera Opened")

def stop_camera():
    global cap, out, recording
    if cap:
        cap.release()
        cap = None
    if recording:
        stop_recording()
    video_label.config(image='')
    status_bar.config(text="Camera Closed")

def start_recording():
    global recording, out, cap
    if cap and not recording:
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20, (w,h))
        recording = True
        record_button.config(text="Stop Recording")
        status_bar.config(text="Recording...")
    elif recording:
        stop_recording()

def stop_recording():
    global recording, out
    recording = False
    if out:
        out.release()
        out = None
    record_button.config(text="Start Recording")
    status_bar.config(text="Recording Stopped")

def take_snapshot():
    if cap:
        ret, frame = cap.read()
        if ret:
            if not os.path.exists("snapshots"):
                os.makedirs("snapshots")
            filename = datetime.datetime.now().strftime("snapshots/snap_%Y%m%d_%H%M%S.jpg")
            cv2.imwrite(filename, frame)
            status_bar.config(text=f"Snapshot saved: {filename}")

def update_frame():
    global cap, recording, out
    if cap:
        ret, frame = cap.read()
        if ret:
            h, w, _ = frame.shape
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_results = face_detection.process(rgb)
            mesh_results = face_mesh.process(rgb)

            # Draw bounding boxes for all detected faces
            if face_results.detections:
                for i, detection in enumerate(face_results.detections):
                    bboxC = detection.location_data.relative_bounding_box
                    x, y, bw, bh = int(bboxC.xmin*w), int(bboxC.ymin*h), int(bboxC.width*w), int(bboxC.height*h)
                    cv2.rectangle(frame, (x, y), (x+bw, y+bh), (255,255,255), 2)
                    cv2.putText(frame, f"Face {i+1}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

            # Draw reduced mesh and label features
            if mesh_results.multi_face_landmarks:
                for landmarks in mesh_results.multi_face_landmarks:
                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing.DrawingSpec(color=(0,255,0), thickness=1, circle_radius=1)
                    )

                    # Nose
                    nose = landmarks.landmark[1]
                    nose_x, nose_y = int(nose.x*w), int(nose.y*h)
                    cv2.circle(frame, (nose_x, nose_y), 5, (0,255,0), -1)
                    cv2.putText(frame, "Nose", (nose_x+5, nose_y-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0),1)

                    # Eyes
                    left_eye = landmarks.landmark[33]
                    right_eye = landmarks.landmark[263]
                    left_x, left_y = int(left_eye.x*w), int(left_eye.y*h)
                    right_x, right_y = int(right_eye.x*w), int(right_eye.y*h)
                    cv2.circle(frame, (left_x,left_y), 5, (255,0,0), -1)
                    cv2.putText(frame, "Left Eye", (left_x+5,left_y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)
                    cv2.circle(frame, (right_x,right_y), 5, (255,0,0), -1)
                    cv2.putText(frame, "Right Eye", (right_x+5,right_y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,0,0),1)

                    # Mouth
                    upper_lip = landmarks.landmark[13]
                    lower_lip = landmarks.landmark[14]
                    mouth_x = int((upper_lip.x + lower_lip.x)/2 * w)
                    mouth_y = int((upper_lip.y + lower_lip.y)/2 * h)
                    cv2.circle(frame, (mouth_x,mouth_y), 5, (0,0,255), -1)
                    cv2.putText(frame, "Mouth", (mouth_x+5,mouth_y-5), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,255),1)

            if recording and out:
                out.write(frame)

            # Display in Tkinter
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        video_label.after(10, update_frame)

# --- GUI ---
root = tk.Tk()
root.title("Face Feature Detection - Multi-Face")
root.geometry("1200x750")
root.configure(bg="#1c1c2e")
DarkStyle(root)

# Close window on 'q' or 'Q'
def close_on_q(event=None):
    stop_camera()
    root.destroy()

root.bind('q', close_on_q)
root.bind('Q', close_on_q)

# Header
header = tk.Label(root, text="Face Feature Detection - Multi-Face", font=('Arial',18,'bold'), bg="#0d1a3a", fg="white")
header.pack(fill=tk.X)

# Main container
main_frame = tk.Frame(root, bg="#1c1c2e")
main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Left - Video
video_frame = tk.Frame(main_frame, bg="black")
video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
video_label = tk.Label(video_frame, bg="black")
video_label.pack(fill=tk.BOTH, expand=True)

# Right - Controls
control_frame = tk.Frame(main_frame, bg="#1c1c2e", width=300)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10,0))

ttk.Button(control_frame, text="Open Camera", command=start_camera).pack(fill=tk.X, pady=5)
ttk.Button(control_frame, text="Close Camera", command=stop_camera).pack(fill=tk.X, pady=5)
record_button = ttk.Button(control_frame, text="Start Recording", command=start_recording)
record_button.pack(fill=tk.X, pady=5)
ttk.Button(control_frame, text="Take Snapshot", command=take_snapshot).pack(fill=tk.X, pady=5)

# Status bar
status_bar = tk.Label(root, text="Ready", bg="#0d1a3a", fg="white", anchor='w')
status_bar.pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
