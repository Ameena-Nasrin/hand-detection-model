# Hand Detection Model

A real-time Hand Detection System built using Python, OpenCV, and MediaPipe.  
This project detects and tracks hand movements using a webcam and serves as a base for applications like AirCanvas, gesture control, and AI-based interaction systems.

---

## Project Overview

This project uses computer vision techniques to:
- Detect hands in real-time  
- Track finger positions  
- Enable interaction using gestures  

It is designed as a beginner to intermediate level project for understanding image processing, hand tracking, and human-computer interaction.

---

## Tech Stack

- Python  
- OpenCV  
- MediaPipe  
- NumPy  

---

## How It Works

The system follows this workflow:

### 1. Video Capture
- Captures real-time video using a webcam  
- Frames are flipped for natural interaction  

### 2. Hand Detection
- MediaPipe detects hand landmarks (21 key points)  
- Tracks position of fingers and palm  

### 3. Processing
- Extracts coordinates of hand landmarks  
- Identifies gestures or movement  

### 4. Output
- Displays hand tracking visually  
- Can be extended to drawing (AirCanvas), gesture control, and virtual interaction  

---

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mhd-humraz/hand-detection-model.git
cd hand-detection-model
```
### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Run the Project
```
python app.py
```

## Important Notes

- Webcam access is required  
- Works best on a local system (not Codespaces)  
- Codespaces may not support camera input and GUI display (`cv2.imshow`)  

---
## Project Structure
```
hand-detection-model
│── app.py                  # Main application entry point
│── hand_tracker.py         # Hand tracking logic using MediaPipe
│── ui_manager.py           # UI handling and drawing logic
│── utils.py                # Helper functions and utilities
│── hand_landmarker.task    # Pre-trained model file for hand detection
│── requirements.txt        # Project dependencies
│── README.md               # Project documentation
│── __pycache__/            # Python cache files (auto-generated)
```
---


## Use Cases

- Virtual drawing applications (AirCanvas)
- Gesture-based system control
- Interactive AI systems
- Educational computer vision projects
---
## Features

- Real-time hand tracking  
- Lightweight and fast  
- Beginner-friendly code  
- Easily extendable  

---

## Future Improvements

- AirCanvas (draw using hand)  
- Gesture-based controls  
- AI gesture recognition  
- Web-based version  

---

## Contributors

- Ameena Nasrin  
- Safa Mariyam  
- Muhammed Humraz  
- Fathima M A

---
## Support

If you found this project useful, consider giving it a star.
---

![Python](https://img.shields.io/badge/Python-3.x-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Tracking-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
