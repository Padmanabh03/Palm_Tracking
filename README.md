# Hand Tracking with Mediapipe

## Project Overview
This project demonstrates a **real-time hand tracking application** using Mediapipe's Hand solutions and OpenCV. The project provides functionality for detecting and tracking hand landmarks, drawing connections between landmarks, and even controlling system volume based on hand gestures. It is structured into multiple Python modules for modularity and reusability.

---

## Features
- **Hand Landmark Detection**: Detects up to 21 landmarks on a hand using Mediapipe.
- **Real-Time Tracking**: Tracks hand movements and updates landmark positions in real time.
- **Volume Control**: Adjusts system volume based on the distance between the thumb and index finger.
- **FPS Calculation**: Displays the frame-per-second (FPS) on the output video feed.
- **Modular Design**: Code is organized into separate files for cleaner and reusable implementation.

---

## File Descriptions

### 1. `Hand_Tracking.py`
This script demonstrates basic hand tracking functionalities:
- Captures video from the webcam.
- Detects and draws hand landmarks.
- Displays FPS on the video feed.
- Press `q` to exit the application.

### 2. `Hand_Tracking_Module.py`
A class-based implementation of hand tracking:
- **HandTracker Class**:
  - Tracks hand landmarks.
  - Provides FPS calculation.
  - Includes a method for volume control using pycaw.
  - Dynamically updates volume based on the distance between the thumb and index finger.
  - Visualizes the volume control bar and percentage in real time.
- Ensures modularity for easy integration into other projects.

### 3. `main_runner.py`
A simple entry point to the project:
- Imports the `HandTracker` class from the module.
- Initiates and runs the hand tracker application.

---

## Dependencies
- **Python 3.8+**
- **OpenCV**: `pip install opencv-python`
- **Mediapipe**: `pip install mediapipe`
- **PyCaw** (optional, for volume control): `pip install pycaw`
- **NumPy**: `pip install numpy`
- **Comtypes**: `pip install comtypes`

---

## Usage

### Running the Scripts
1. Clone or download the repository.
2. Install the required dependencies using:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the following command to start the application:
   ```bash
   python main_runner.py
   ```

### Controls
- Use gestures to control system volume:
  - **Thumb-Index Distance**: Changes volume based on the distance between thumb and index finger.
  - **Close Fingers**: Mute the system volume.

- Press `q` to quit the application.

---

## Key Implementation Details
- **Hand Landmark Tracking**: Powered by Mediapipe's efficient hand detection model.
- **Volume Control**: Uses pycaw to interface with system audio settings.
- **Real-Time Performance**: Optimized for high FPS, ensuring smooth tracking and control.

---

## Future Improvements
- Add gesture-based controls for more system functions.
- Enhance robustness of hand detection under varying lighting conditions.
- Support multiple languages for the user interface.
- Extend functionality to detect hand gestures for gaming or productivity tools.

---

## License
This project is open-source and available under the MIT License.

--- 
