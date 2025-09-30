import cv2
import time
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys

# --- Globals ---
cap = None
is_recording = False
recorder = None
blur_enabled = True
prev_time = 0
last_faces = []
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
output_dir = "recordings"
os.makedirs(output_dir, exist_ok=True)

# Haar Cascade (use full path here)
face_cascade = cv2.CascadeClassifier(
    r"C:\Users\Safan\OneDrive\Desktop\Safan's Projects\assignment internship\part B Q4 blurred face\haarcascade_frontalface_default.xml"
)

# --- Helper Functions ---
def make_filename():
    t = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(output_dir, f"recording_{t}.mp4")

def pixelate_face(roi, blocks=15):
    h, w = roi.shape[:2]
    temp = cv2.resize(roi, (blocks, blocks), interpolation=cv2.INTER_LINEAR)
    return cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

# --- Camera Functions ---
def start_camera():
    global cap
    if cap is None:
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not cap.isOpened():
            status_label.config(text="Error: Camera not found", foreground="#ff4d6d")
            return
        update_frame()
        status_label.config(text="Camera Opened", foreground="#00ffea")

def stop_camera():
    global cap, recorder, is_recording
    if cap:
        cap.release()
        cap = None
    if is_recording:
        stop_recording()
    video_label.config(image='')
    status_label.config(text="Camera Closed", foreground="#ff4d6d")

def toggle_blur():
    global blur_enabled
    blur_enabled = not blur_enabled
    blur_button.config(text="Blur ON" if blur_enabled else "Blur OFF")
    status_label.config(text=f"Blur {'Enabled' if blur_enabled else 'Disabled'}", foreground="#00ffea")

def start_recording():
    global is_recording, recorder, cap
    if cap and not is_recording:
        ret, frame = cap.read()
        if ret:
            height, width = frame.shape[:2]
            filename = make_filename()
            recorder = cv2.VideoWriter(filename, fourcc, 20.0, (width, height))
            is_recording = True
            record_button.config(text="Stop Recording")
            status_label.config(text=f"Recording Started -> {filename}", foreground="#00ffea")
    elif is_recording:
        stop_recording()

def stop_recording():
    global is_recording, recorder
    is_recording = False
    if recorder:
        recorder.release()
        recorder = None
    record_button.config(text="Start Recording")
    status_label.config(text="Recording Stopped", foreground="#ffae42")

def update_frame():
    global cap, prev_time, last_faces, is_recording, recorder
    if cap:
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60)
            )
            if len(faces) == 0 and len(last_faces) > 0:
                faces = last_faces
            else:
                last_faces = faces

            if blur_enabled:
                for (x, y, w, h) in faces:
                    roi = frame[y:y+h, x:x+w]
                    roi_pix = pixelate_face(roi, blocks=20)
                    roi_blur = cv2.GaussianBlur(roi_pix, (51, 51), 30)
                    frame[y:y+h, x:x+w] = roi_blur

            # FPS
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if prev_time else 0
            prev_time = curr_time
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

            if is_recording:
                cv2.putText(frame, "REC", (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)
                if recorder:
                    recorder.write(frame)

            # Resize to fit label without hiding buttons
            label_width = video_label.winfo_width()
            label_height = video_label.winfo_height()
            if label_width > 0 and label_height > 0:
                frame = cv2.resize(frame, (label_width, label_height))

            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame_rgb)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)

        video_label.after(10, update_frame)

def close_app(event=None):
    stop_camera()
    if recorder:
        recorder.release()
    root.destroy()
    sys.exit()

# --- GUI ---
root = tk.Tk()
root.title("Face Pixelation & Recording")
root.geometry("1200x800")
root.config(bg="#1b1b2f")  # Dark blue-black

# Configure grid
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)  # Button frame
root.columnconfigure(0, weight=1)

# Video Frame (fills space above buttons)
video_label = tk.Label(root, bg="#0a0a23")
video_label.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

# Button Frame (always visible at bottom)
button_frame = tk.Frame(root, bg="#1b1b2f")
button_frame.grid(row=1, column=0, pady=10)

style = ttk.Style()
style.theme_use('clam')
style.configure('TButton', font=('Arial', 12, 'bold'), foreground='white', background='#0055ff')
style.map('TButton', background=[('active', '#0088ff')])

open_button = ttk.Button(button_frame, text="Open Camera", command=start_camera)
open_button.grid(row=0, column=0, padx=10)

close_button = ttk.Button(button_frame, text="Close Camera", command=stop_camera)
close_button.grid(row=0, column=1, padx=10)

blur_button = ttk.Button(button_frame, text="Blur ON", command=toggle_blur)
blur_button.grid(row=0, column=2, padx=10)

record_button = ttk.Button(button_frame, text="Start Recording", command=start_recording)
record_button.grid(row=0, column=3, padx=10)

status_label = tk.Label(root, text="Status: Idle", bg="#1b1b2f", fg="white", font=("Arial", 12))
status_label.grid(row=2, column=0, pady=5)

# Bind 'q' key to close entire app
root.bind("<Key>", lambda e: close_app() if e.char.lower() == 'q' else None)
root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()
