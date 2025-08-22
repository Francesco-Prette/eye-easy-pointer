import cv2
import numpy as np
import pyautogui

def compute_affine_transform(eye_points, screen_points):
    """Find affine transformation between eye and screen points."""
    return cv2.estimateAffine2D(np.array(eye_points), np.array(screen_points))[0]

def map_eye_to_screen(eye, transform):
    """Apply affine transform to map eye position to screen coords."""
    eye_coords = np.array([[eye[0], eye[1]]])
    mapped = cv2.transform(np.array([eye_coords]), transform)[0][0]
    return mapped

def move_mouse(x, y):
    """Move mouse to mapped coordinates."""
    pyautogui.moveTo(x, y)
