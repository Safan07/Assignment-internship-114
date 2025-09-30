import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# === Paths ===
image_folder = 'images'
label_folder = 'labels'

# === Class Names ===
class_names = {0: 'plate', 1: 'character intact', 2: 'character broken'}

# === GUI Initialize ===
root = tk.Tk()
root.title("License Plate Character Break Detection")
root.geometry("1400x900")
root.minsize(1200, 800)
root.configure(bg="#0D1117")

# === Top Frame (Info Labels) ===
top_frame = tk.Frame(root, bg="#0D1117")
top_frame.pack(side='top', fill='x', padx=15, pady=5)
info_label = tk.Label(top_frame, text="", bg="#0D1117", fg="#39A2DB", font=('Helvetica', 13))
info_label.pack(side='top', pady=2)
plate_status_label = tk.Label(top_frame, text="", bg="#0D1117", font=('Helvetica', 15, 'bold'))
plate_status_label.pack(side='top', pady=2)

# === Middle Frame (Image Canvas) ===
img_frame = tk.Frame(root, bg="#0D1117")
img_frame.pack(fill='both', expand=True, padx=20, pady=10)

img_canvas = tk.Canvas(img_frame, bg="#161B22", highlightthickness=0)
img_canvas.pack(fill='both', expand=True)

# Image label
img_label = tk.Label(img_canvas, bg="#161B22")
img_window = img_canvas.create_window(0, 0, window=img_label, anchor='nw')

# Scrollbars
img_scroll_y = tk.Scrollbar(img_frame, orient="vertical", command=img_canvas.yview)
img_scroll_x = tk.Scrollbar(img_frame, orient="horizontal", command=img_canvas.xview)
img_canvas.configure(yscrollcommand=img_scroll_y.set, xscrollcommand=img_scroll_x.set)
img_scroll_y.pack(side='right', fill='y')
img_scroll_x.pack(side='bottom', fill='x')

# === Bottom Frame (Buttons) ===
button_frame = tk.Frame(root, bg="#0D1117")
button_frame.pack(side='top', fill='x', padx=15, pady=5)

def on_enter(e):
    e.widget['bg'] = '#1659B5'
def on_leave(e):
    e.widget['bg'] = '#1F6FEB'

prev_btn = tk.Button(button_frame, text="<< Previous", bg="#1F6FEB", fg="white",
                     font=('Helvetica', 12, 'bold'), padx=15, pady=6, relief='flat', bd=0)
prev_btn.pack(side='left', padx=10)
prev_btn.bind("<Enter>", on_enter)
prev_btn.bind("<Leave>", on_leave)

next_btn = tk.Button(button_frame, text="Next >>", bg="#1F6FEB", fg="white",
                     font=('Helvetica', 12, 'bold'), padx=15, pady=6, relief='flat', bd=0)
next_btn.pack(side='left', padx=10)
next_btn.bind("<Enter>", on_enter)
next_btn.bind("<Leave>", on_leave)

# === Summary Table ===
summary_frame = tk.Frame(root, bg="#0D1117")
summary_frame.pack(side='top', fill='both', expand=True, padx=15, pady=10)
columns = ('Filename', 'Intact', 'Broken', 'Plate Status')

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                background="#161B22",
                foreground="white",
                fieldbackground="#161B22",
                font=('Helvetica', 11))
style.configure("Treeview.Heading",
                background="#1F6FEB",
                foreground="white",
                font=('Helvetica', 12, 'bold'))
style.map('Treeview',
          background=[('selected', '#39A2DB')],
          foreground=[('selected', 'black')])

tree = ttk.Treeview(summary_frame, columns=columns, show='headings', height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200, anchor='center')
tree.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(summary_frame, orient='vertical', command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side='right', fill='y')

# === Load Images ===
image_files = [f for f in os.listdir(image_folder) if f.lower().endswith(('.jpg','.png','.jpeg'))]
current_index = 0

# === Process Image Function ===
def process_image(image_file):
    img_path = os.path.join(image_folder, image_file)
    label_path = os.path.join(label_folder, os.path.splitext(image_file)[0]+'.txt')
    img = cv2.imread(img_path)
    if img is None:
        return None, 0, 0, "Cannot read image"
    h, w = img.shape[:2]
    intact_count = 0
    broken_count = 0
    if not os.path.exists(label_path):
        return img, 0, 0, "No label file"
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            cls, x_center, y_center, bw, bh = map(float, parts)
            cls = int(cls)
            x_center *= w
            y_center *= h
            bw *= w
            bh *= h
            x1 = int(x_center - bw / 2)
            y1 = int(y_center - bh / 2)
            x2 = int(x_center + bw / 2)
            y2 = int(y_center + bh / 2)
            color = (255,0,0) if cls==0 else (0,255,0) if cls==1 else (0,0,255)
            cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
            cv2.putText(img, class_names[cls], (x1, y1-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
            if cls==1: intact_count+=1
            elif cls==2: broken_count+=1
    plate_status = "Intact" if broken_count==0 else "Broken"
    return img, intact_count, broken_count, plate_status

# === Show Image Function ===
def show_image(idx):
    if idx < 0 or idx >= len(image_files):
        return
    image_file = image_files[idx]
    img, intact_count, broken_count, plate_status = process_image(image_file)
    if img is None:
        info_label.config(text=f"Cannot read {image_file}")
        plate_status_label.config(text="")
        img_label.config(image='')
        return

    info_label.config(text=f"{image_file}: {intact_count} intact, {broken_count} broken characters")
    plate_status_label.config(text=f"Overall Plate: {plate_status}",
                              fg="#39A2DB" if plate_status=="Intact" else "#DC3545")

    canvas_width = max(img_canvas.winfo_width(), 10)
    canvas_height = max(img_canvas.winfo_height(), 10)
    h, w = img.shape[:2]
    scale_w = canvas_width * 0.95 / w
    scale_h = canvas_height * 0.95 / h
    scale = min(scale_w, scale_h, 2.0)  # increase max scale for larger image

    new_w = max(int(w * scale), 1)
    new_h = max(int(h * scale), 1)
    img_resized = cv2.resize(img, (new_w, new_h))

    img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    img_tk = ImageTk.PhotoImage(img_pil)
    img_label.imgtk = img_tk
    img_label.config(image=img_tk)

    x_offset = max((canvas_width - new_w)//2, 0)
    y_offset = max((canvas_height - new_h)//2, 0)
    img_canvas.coords(img_window, x_offset, y_offset)
    img_canvas.config(scrollregion=(0,0,max(new_w, canvas_width), max(new_h, canvas_height)))

# === Populate Table ===
for image_file in image_files:
    img, intact_count, broken_count, plate_status = process_image(image_file)
    tag = 'intact' if plate_status=="Intact" else 'broken'
    tree.insert('', tk.END, values=(image_file, intact_count, broken_count, plate_status), tags=(tag,))
tree.tag_configure('intact', background='#0D6EFD')
tree.tag_configure('broken', background='#DC3545')

# === Navigation Buttons ===
def next_image():
    global current_index
    current_index = (current_index + 1) % len(image_files)
    show_image(current_index)
def prev_image():
    global current_index
    current_index = (current_index - 1) % len(image_files)
    show_image(current_index)
prev_btn.config(command=prev_image)
next_btn.config(command=next_image)

# === Start GUI ===
show_image(current_index)
root.mainloop()
