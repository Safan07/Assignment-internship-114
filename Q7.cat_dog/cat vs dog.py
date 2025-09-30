import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import torch
from torchvision import models, transforms
from PIL import Image, ImageTk
import os

class DarkStyle(ttk.Style):
    def __init__(self, root):
        super().__init__(root)
        self.theme_use('clam')
        self.configure('.', background='#1c1c2e', foreground='white', font=('Arial', 10))
        self.configure('Treeview', background='#2e2e44', foreground='white', fieldbackground='#2e2e44')
        self.configure('Treeview.Heading', background='#0d1a3a', foreground='white', font=('Arial', 10, 'bold'))
        self.map('TButton',
                 foreground=[('active', 'white')],
                 background=[('active', '#0055ff')])

class CatDogClassifierGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Cat vs Dog Classifier")
        self.root.geometry("1000x700")
        self.root.configure(bg="#1c1c2e")
        DarkStyle(self.root)

        self.model = None
        self.class_labels = {}
        self.setup_model()
        self.image_paths = []

        self.setup_gui()

    def setup_model(self):
        try:
            self.model = models.resnet50(pretrained=True)
            self.model.eval()
            self.load_imagenet_labels()
            self.preprocess = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406],
                    std=[0.229, 0.224, 0.225]
                )
            ])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load model: {e}")

    def load_imagenet_labels(self):
        self.class_labels = {281:'tabby cat', 282:'tiger cat',283:'persian cat',284:'siamese cat',285:'egyptian cat',
                             151:'chihuahua',152:'japanese spaniel',153:'maltese dog',154:'pekinese',155:'shih-tzu'}
        dog_breeds = {160:'afghan hound',161:'basset',162:'beagle',163:'bloodhound',164:'bluetick'}
        self.class_labels.update(dog_breeds)

    def setup_gui(self):
        self.header = tk.Label(self.root, text="Cat vs Dog Classification",
                               font=('Arial', 18, 'bold'), bg="#0d1a3a", fg="white")
        self.header.pack(fill=tk.X, pady=(0,10))

        main_frame = tk.Frame(self.root, bg="#1c1c2e")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Left frame - buttons and image list
        left_frame = tk.Frame(main_frame, bg="#1c1c2e")
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0,10))

        ttk.Label(left_frame, text="Selected Images:").pack(anchor='w', pady=(0,5))
        self.image_listbox = tk.Listbox(left_frame, width=35, height=25, bg='#2e2e44', fg='white')
        self.image_listbox.pack(fill=tk.Y, expand=False)

        button_frame = tk.Frame(left_frame, bg="#1c1c2e")
        button_frame.pack(pady=15, fill=tk.X)

        self.add_btn = ttk.Button(button_frame, text="Add Images", command=self.add_images)
        self.add_btn.pack(side=tk.TOP, pady=3, fill=tk.X)
        self.clear_btn = ttk.Button(button_frame, text="Clear All", command=self.clear_images)
        self.clear_btn.pack(side=tk.TOP, pady=3, fill=tk.X)
        self.analyze_btn = ttk.Button(button_frame, text="Analyze Images", command=self.analyze_images)
        self.analyze_btn.pack(side=tk.TOP, pady=3, fill=tk.X)

        # Right frame - results tree on top, preview below
        right_frame = tk.Frame(main_frame, bg="#1c1c2e")
        right_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        ttk.Label(right_frame, text="Results:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(0,5))

        columns = ('Image','True Label','Predicted','Confidence','Status')
        self.results_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=18)
        for col in columns:
            self.results_tree.heading(col, text=col)
            self.results_tree.column(col, width=150)
        self.results_tree.pack(fill=tk.BOTH, expand=True, pady=(0,10))

        scrollbar = ttk.Scrollbar(self.results_tree, orient=tk.VERTICAL, command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.image_label = tk.Label(right_frame, text="Image preview will appear here", bg="#1c1c2e", fg="white")
        self.image_label.pack(fill=tk.BOTH, expand=True, pady=5)

        self.status_bar = tk.Label(self.root, text="Ready", bg="#0d1a3a", fg="white", anchor='w')
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.results_tree.bind('<<TreeviewSelect>>', self.show_selected_image)

    def add_images(self):
        files = filedialog.askopenfilenames(title="Select images",
                                            filetypes=[("Image files","*.jpg *.jpeg *.png *.bmp")])
        for file_path in files:
            if file_path not in self.image_paths:
                self.image_paths.append(file_path)
                self.image_listbox.insert(tk.END, os.path.basename(file_path))

    def clear_images(self):
        self.image_paths.clear()
        self.image_listbox.delete(0, tk.END)
        self.clear_results()

    def clear_results(self):
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        self.image_label.configure(image='', text="Image preview will appear here")
        self.status_bar.config(text="Ready")

    def classify_image(self, image_path):
        try:
            image = Image.open(image_path).convert('RGB')
            input_tensor = self.preprocess(image)
            input_batch = input_tensor.unsqueeze(0)
            with torch.no_grad():
                output = self.model(input_batch)
            probabilities = torch.nn.functional.softmax(output[0], dim=0)
            top_prob, top_catid = torch.topk(probabilities, 1)
            class_id = top_catid[0].item()
            class_name = self.class_labels.get(class_id, f"class_{class_id}")
            confidence = top_prob[0].item()
            return class_name, confidence, image
        except:
            return None, None, None

    def is_dog_breed(self, class_name):
        dog_indicators = ['dog','hound','terrier','retriever','spaniel','sheepdog','bulldog','poodle']
        return any(indicator in class_name.lower() for indicator in dog_indicators)

    def analyze_images(self):
        if not self.image_paths:
            messagebox.showwarning("Warning","Please add images first!")
            return
        self.clear_results()
        misclassified_count = 0

        for image_path in self.image_paths:
            filename = os.path.basename(image_path)
            predicted_class, confidence, image = self.classify_image(image_path)
            if predicted_class:
                true_label = "Dog"
                is_dog = self.is_dog_breed(predicted_class)
                status = "Correct" if is_dog else "Misclassified"
                if not is_dog:
                    misclassified_count += 1
                self.results_tree.insert('', tk.END, values=(filename,true_label,predicted_class,f"{confidence:.2%}",status),
                                         tags=(status,))
        self.results_tree.tag_configure('Misclassified', background='#ff5555')
        self.results_tree.tag_configure('Correct', background='#55ff55')
        self.status_bar.config(text=f"Analysis done! Misclassified: {misclassified_count} / {len(self.image_paths)}")

    def show_selected_image(self,event):
        selection = self.results_tree.selection()
        if not selection:
            return
        item = selection[0]
        values = self.results_tree.item(item, 'values')
        filename = values[0]
        image_path = None
        for path in self.image_paths:
            if os.path.basename(path) == filename:
                image_path = path
                break
        if image_path:
            image = Image.open(image_path)
            image.thumbnail((400,400))
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo,text="")
            self.image_label.image = photo

def main():
    root = tk.Tk()
    app = CatDogClassifierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
