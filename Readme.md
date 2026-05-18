# Hand Gesture for Smart IoT Lighting

A real-time, touchless home automation system bridging computer vision and embedded systems to control physical hardware using hand gestures. By leveraging Google's MediaPipe framework for real-time edge-based hand tracking and an Arduino Uno for hardware control, this project provides a hygienic and accessible alternative to traditional physical switches.

---

## Key Features
* **Real-Time Landmark Tracking**: Extracts 21 3D hand coordinates using MediaPipe Hands, operating with an average latency of just 50–100ms.
* **Dual Firmware Operational Modes**: Features two distinct Arduino control setups:
  * `SingleLED`: State-based triggering to selectively activate a single matching LED corresponding to the exact finger count.
  * `MultipleLED`: Sequential subset illumination (e.g., raising 3 fingers lights up 3 LEDs simultaneously).
* **Hardware-in-the-Loop (HIL)**: Robust integration using Python serial communication to stream real-time coordinate state changes straight to an Arduino Uno microcontroller over a USB connection.

---

## System Demo

> **Note:** The architecture processes live webcam frames and matches direct breadboard LED feedback loops instantly.

---

## System Architecture & Hardware

### Software Pipeline
1. **Frame Capture**: Continuous live webcam frames are ingested via OpenCV.
2. **Gesture Inference**: Frames are processed by MediaPipe Hands to isolate finger positions relative to lower joints.
3. **Serial Stream**: The dynamic finger count string is written to the active serial port via PySerial.
4. **Hardware Execution**: The Arduino interprets the incoming byte array using `Serial.parseInt()` to update digital pin outputs (Pins 9–13).

### Hardware Components
* Arduino Uno
* Half-Size Breadboard
* 5x LEDs (Blue, Green, Yellow, 2x Red)
* 5x 220Ω Current-Limiting Resistors
* Jumper Wires & USB Interface Cable

---

## Engineering Insights: Overcoming Challenges

### Pivoting from YOLOv5 to MediaPipe Hands
Initially, the system was architected around a custom-trained YOLOv5 pipeline, requiring manual dataset labeling and annotation of approximately 2,000 images. However, during mid-project evaluations, deployment testing revealed edge-case hardware bottlenecks and accuracy drops on standard runtime computing environments. 

To optimize performance and meet strict latency goals, the system architecture was refactored to utilize **MediaPipe Hands**. This pivot eliminated model execution lag, driving the system tracking accuracy up to **95% under standard conditions** and reducing final processing latency to a seamless **50–100ms window**.

---

## Getting Started

### Prerequisites
Ensure your machine has Python 3.8+ installed.

### Installation & Execution
1. **Clone this repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git)
   cd Arduino
2. **Install the Python dependencies**
   ```bash
   pip install opencv-python mediapipe pyserial
3. **Upload Firmware**
   Open the Arduino IDE, load either the SingleLED/SingleLED.ino or MultipleLED/MultipleLED.ino sketch, and upload it to your Arduino Uno.
4. **Run the Controller Script:**
   Verify your active Arduino COM port in gesture_recognition.py (default is set to 'COM3') and run the script:
   ```bash
   python gesture_recognition.py
