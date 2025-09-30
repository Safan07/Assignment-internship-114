# Q6: Automated License Plate Testing

## Overview

This project performs **automated testing** of Indian license plate recognition using Python and Pytest.  
It validates the program developed in Q5 by testing **valid** and **invalid** license plate strings.

- **Valid plates** should match perfectly (100% similarity).  
- **Invalid plates** should differ (similarity < 100%).

Similarity is calculated using Python's `difflib.SequenceMatcher`.

---

## Features

- **Random Valid Plate Generation**  
  Generates realistic Indian license plates in the format:  
XX00XX0000

markdown
Copy code
where:  
- `XX` → State code (letters)  
- `00` → District code (digits)  
- `XX` → Series code (letters)  
- `0000` → Number (1–9999)  

- **Random Invalid Plate Generation**  
Slightly modifies valid plates to simulate recognition errors.

- **Automated Pytest Testing**  
- 1000 tests in total (500 valid + 500 invalid)  
- Checks similarity alignment for each plate  
- Provides a clear summary of total tests and pass/fail status

---

## Installation

1. Clone the repository or copy the project files.  
2. Install dependencies:

```bash
pip install pytest
Usage
Run the tests:

bash
Copy code
python q6_main_code.py
Expected output:

markdown
Copy code
Running Automated License Plate Tests...

=== CUSTOM SUMMARY ===
Total tests executed: 1000
All tests passed ✅
=====================
How It Works
Generates 500 valid license plates using random_valid_plate().

Generates 500 invalid license plates using random_invalid_plate().

Compares valid plates to themselves → should have 100% similarity.

Compares valid plates to invalid plates → should have <100% similarity.

Uses Pytest to automate the tests and provide verbose results.

Notes
The failure chance for invalid plates (failure_chance=0.05) simulates occasional accidental matches.

Useful for testing license plate recognition models or validation functions.