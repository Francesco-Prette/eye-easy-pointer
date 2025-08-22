import cv2
import numpy as np
from config import SCREEN_W, SCREEN_H, CALIBRATION_POINTS

def show_calibration_dot(idx):
    """Create fullscreen black screen with a red calibration dot."""
    calib_screen = np.zeros((SCREEN_H, SCREEN_W, 3), dtype=np.uint8)
    cx, cy = CALIBRATION_POINTS[idx]
    cv2.circle(calib_screen, (cx, cy), 20, (0, 0, 255), -1)
    cv2.putText(calib_screen, "Look at the dot & press SPACE",
                (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    return calib_screen

def record_eye_position(results, w, h):
    """Extract right iris landmark (index 474)."""
    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark
        return [landmarks[474].x * w, landmarks[474].y * h]
    return None
