# String Similarity Checker

## Overview
This Python application compares two input strings and calculates a **percentage similarity** between them. It also generates a detailed **match report** and **visual alignment**, highlighting matching and mismatching characters. The GUI is built with **Tkinter** and features multiple tabs for clarity.

---

## Features

- **Similarity Percentage**: Shows how similar the two strings are.
- **Visual Alignment**: Displays aligned strings with matching characters highlighted in green and mismatches in red.
- **Detailed Match Report**: Line-by-line report showing matches, mismatches, insertions, and deletions.
- **Summary Tab**: Total characters compared, number of matches, and number of mismatches.
- **Interactive GUI**: Clean interface with tabs for easy navigation.
- **Keyboard Shortcut**: Press **Q** to exit the application.

---

## Requirements

- Python 3.8+
- Tkinter (built-in)
- `difflib` (standard library)

No additional packages are required.

---

## Usage

1. **Run the application**:

```bash
python string_similarity_gui.py
Enter Strings:

Input two strings (6–10 characters each) in the text boxes.

Check Similarity:

Click the Check Similarity button to compute similarity, view alignment, and generate reports.

Tabs:

Tab	Description
Similarity	Displays percentage similarity between strings
Visual Alignment	Shows aligned strings with color-coded matches
Match Report	Detailed line-by-line comparison report
Summary	Overall statistics (total chars, matches, mismatches)

Example
Input 1: hello123

Input 2: h3llo12z

Similarity Tab: 87.5%
Visual Alignment Tab:

nginx
Copy code
h e l l o 1 2 3
| | | | | | | .
h 3 l l o 1 2 z
Match Report Tab: Shows which characters matched, mismatched, inserted, or deleted.
Summary Tab: Total chars = 8, Matches = 7, Mismatches = 1

File Structure
bash
Copy code
project/
│
├─ string_similarity_gui.py  # Main Python script
└─ README.md                 # Project documentation
Notes
Designed for strings 6–10 characters long.

Matching is case-sensitive.

Visual alignment helps in understanding character-level differences.

License
This project is open-source and free to use for educational purposes.
