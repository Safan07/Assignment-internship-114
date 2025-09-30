# Q7: Cat vs Dog Classification (Pre-trained Model)

## Overview

This project implements a **Cat vs Dog image classifier** using a pre-trained **ResNet50** model from ImageNet.  
A **Tkinter GUI** allows users to upload images, view predictions, and analyze misclassifications.

- Uses a pre-trained ImageNet model (`torchvision.models.resnet50`).  
- Preprocesses images for model input (resize, crop, normalize).  
- Displays predicted class, confidence, and highlights misclassified images.  
- Supports batch analysis of multiple images.

---

## Features

- **Graphical User Interface (GUI)**  
  - Dark-themed, user-friendly interface using `tkinter` and `ttk`.  
  - Displays selected images, analysis results, and image previews.  
  - Status bar shows analysis summary.

- **Image Analysis**  
  - Classifies images using ResNet50.  
  - Shows predicted class, confidence, and correctness (dog/cat).  
  - Misclassified images highlighted in red, correct ones in green.

- **Batch Processing**  
  - Add multiple images at once.  
  - Clear images and results easily.  
  - View detailed results in a tree table.

---

## Installation

1. Clone the repository or copy the project files.  
2. Install dependencies:
```bash
pip install torch torchvision pillow
Usage
Run the GUI:

bash
Copy code
python cat_dog_classifier_gui.py
Workflow
Click "Add Images" to select images for classification.

Click "Analyze Images" to classify all selected images.

View results in the right panel:

Filename

True Label (assumed "Dog")

Predicted Class

Confidence (%)

Status (Correct / Misclassified)

Click a row to preview the corresponding image.

Clear images or results with the "Clear All" button.

Sample Results
Five sample images were collected where dogs were misclassified by the model.

Misclassifications typically occurred with breeds not included in the custom label list or when images were atypical (e.g., small dogs, unusual poses).

Image Filename	True Label	Predicted Class	Confidence	Status
dog1.jpg	Dog	cat	72%	Misclassified
dog2.jpg	Dog	fox	65%	Misclassified
dog3.jpg	Dog	wolf	80%	Misclassified
dog4.jpg	Dog	cat	55%	Misclassified
dog5.jpg	Dog	raccoon	60%	Misclassified

Note: Confidence percentages represent the model's top prediction probability.

Notes
The classifier uses pre-trained ImageNet labels and is not fine-tuned for all dog breeds.

Misclassifications are expected for images outside the most common breeds.

This GUI provides a visual tool for analyzing classification results and identifying limitations of the pre-trained model.

License
This project is for educational and internship purposes. Use responsibly.

pgsql
Copy code
