import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import urllib.request
import os

# ── Download the hand landmark model if not present ───────────────────────────
MODEL_PATH = "hand_landmarker.task"
if not os.path.exists(MODEL_PATH):
    print("Downloading hand landmark model...")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task",
        MODEL_PATH
    )
    print("Model downloaded!")

# ── Setup MediaPipe Hand Landmarker ───────────────────────────────────────────
base_options  = python.BaseOptions(model_asset_path=MODEL_PATH)
options       = vision.HandLandmarkerOptions(
                    base_options=base_options,
                    num_hands=1,
                    min_hand_detection_confidence=0.5,
                    min_hand_presence_confidence=0.5,
                    min_tracking_confidence=0.5
                )
landmarker = vision.HandLandmarker.create_from_options(options)

# ── Canvas & drawing state ─────────────────────────────────────────────────────
canvas         = None
draw_color     = (0, 0, 255)   # Red in BGR
brush_size     = 8
prev_x, prev_y = None, None

# ── Open webcam ────────────────────────────────────────────────────────────────
cap = cv2.VideoCapture(0)
print("Air Canvas running!  Press 'c' to clear  |  'q' to quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame      = cv2.flip(frame, 1)
    h, w, _    = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # ── Hand detection with new API ────────────────────────────────────────────
    rgb_frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image   = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    result     = landmarker.detect(mp_image)

    finger_x, finger_y = None, None

    if result.hand_landmarks:
        landmarks = result.hand_landmarks[0]   # first hand

        # Draw all landmark dots on the frame
        for lm in landmarks:
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(frame, (cx, cy), 4, (0, 255, 0), -1)

        # Draw connections between landmarks
        CONNECTIONS = [
            (0,1),(1,2),(2,3),(3,4),
            (0,5),(5,6),(6,7),(7,8),
            (5,9),(9,10),(10,11),(11,12),
            (9,13),(13,14),(14,15),(15,16),
            (13,17),(17,18),(18,19),(19,20),(0,17)
        ]
        for a, b in CONNECTIONS:
            ax, ay = int(landmarks[a].x * w), int(landmarks[a].y * h)
            bx, by = int(landmarks[b].x * w), int(landmarks[b].y * h)
            cv2.line(frame, (ax, ay), (bx, by), (0, 255, 0), 2)

        # Landmark 8 = index fingertip
        finger_x = int(landmarks[8].x * w)
        finger_y = int(landmarks[8].y * h)

        # Highlight the fingertip
        cv2.circle(frame, (finger_x, finger_y), 10, draw_color, -1)

    # ── Drawing logic ──────────────────────────────────────────────────────────
    if finger_x is not None and finger_y is not None:
        if prev_x is not None and prev_y is not None:
            cv2.line(canvas, (prev_x, prev_y),
                              (finger_x, finger_y), draw_color, brush_size)
        prev_x, prev_y = finger_x, finger_y
    else:
        prev_x, prev_y = None, None

    # ── Merge canvas onto live frame ───────────────────────────────────────────
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, mask     = cv2.threshold(gray_canvas, 1, 255, cv2.THRESH_BINARY)
    frame[mask == 255] = canvas[mask == 255]

    # ── Instructions ───────────────────────────────────────────────────────────
    cv2.putText(frame, "Q: Quit | C: Clear", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Air Canvas", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('c'):
        canvas = np.zeros((h, w, 3), dtype=np.uint8)
        print("Canvas cleared!")

# ── Cleanup ────────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()