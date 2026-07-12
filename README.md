# 🎨 Air Canvas

An AI-powered virtual drawing application that allows users to draw on a digital canvas using hand gestures captured through a webcam. The project uses real-time hand landmark detection to replace traditional mouse or pen input with intuitive finger movements.

## 📌 Features

* ✋ Real-time hand tracking using AI
* 🎨 Draw on a virtual canvas with finger gestures
* 📷 Webcam-based interaction
* ⚡ Smooth and responsive drawing experience
* 🖌️ Multiple drawing colors
* 🧹 Clear canvas functionality

## 🛠️ Technologies Used

* Python
* OpenCV
* MediaPipe Tasks (Hand Landmarker)
* NumPy

## 📂 Project Structure

```text
air_canvas/
│── air_canvas.py          # Main application
│── hand_landmarker.task   # MediaPipe hand landmark model
│── README.md
```

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/Sijenna/air_canvas.git
```

### 2. Navigate to the project

```bash
cd air_canvas
```

### 3. Install the required libraries

```bash
pip install opencv-python mediapipe numpy
```

## ▶️ Run the Project

```bash
python air_canvas.py
```

Ensure your webcam is connected before launching the application.

## 🎯 How It Works

1. The webcam captures live video.
2. MediaPipe detects the user's hand landmarks.
3. The fingertip position is tracked in real time.
4. Finger movements are translated into drawing strokes on the virtual canvas.
5. Users can switch colors and clear the canvas using gesture-based controls.

## 📸 Demo

You can add screenshots or a GIF here to demonstrate the application.

Example:

```
images/demo.gif
```

or

```
images/screenshot.png
```

## 📈 Future Improvements

* Adjustable brush size
* Eraser mode
* Save drawings as images
* Gesture shortcuts
* Undo and redo functionality
* Multi-hand support

## 🤝 Contributing

Contributions are welcome. Feel free to fork the repository, create a feature branch, and submit a pull request.

## 📄 License

This project is available under the MIT License.

## 👩‍💻 Author

**Sijenna**

GitHub: https://github.com/Sijenna
