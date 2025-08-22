import cv2
import mediapipe as mp
import keyboard
import pyautogui
from screeninfo import get_monitors

from scripts.utils import create_fullscreen_window
from scripts.calibration import show_calibration_dot, record_eye_position
from scripts.tracking import compute_affine_transform, map_eye_to_screen, move_mouse

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

# Mediapipe setup
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Screen size
SCREEN_W, SCREEN_H = pyautogui.size()

# Calibration points (corners + center)
CALIBRATION_POINTS = [
    (0, 0),
    (SCREEN_W - 1, 0),
    (0, SCREEN_H - 1),
    (SCREEN_W - 1, SCREEN_H - 1),
    (SCREEN_W // 2, SCREEN_H // 2)
]
print(SCREEN_W, SCREEN_H)

# Camera
cam = cv2.VideoCapture(0)
create_fullscreen_window()

# Calibration state
calibration_points_eye = []
calibrated = False
current_calibration_idx = 0
transform = None

print("Calibration started: look at the red dot when shown")
print("Press SPACE to calibrate a point, ESC to exit, or SHIFT+ESC to force stop")

while True:
    if keyboard.is_pressed("shift+esc"):
        print("Force stop triggered!")
        break

    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)
    h, w, _ = frame.shape

    if not calibrated and current_calibration_idx < len(CALIBRATION_POINTS):
        # Show calibration screen
        calib_screen = show_calibration_dot(current_calibration_idx, SCREEN_W, SCREEN_H, CALIBRATION_POINTS)
        cv2.imshow("Calibration", calib_screen)
    else:
        # Tracking mode
        eye = record_eye_position(results, w, h)
        if eye and calibrated and transform is not None:
            mapped = map_eye_to_screen(eye, transform)
            move_mouse(mapped[0], mapped[1])

        cv2.imshow("Eye Mouse", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC
        break
    elif key == 32 and not calibrated:  # SPACE
        eye = record_eye_position(results, w, h)
        if eye:
            calibration_points_eye.append(eye)
            current_calibration_idx += 1
            if current_calibration_idx >= len(CALIBRATION_POINTS):
                transform = compute_affine_transform(calibration_points_eye, CALIBRATION_POINTS)
                calibrated = True
                print("Calibration complete!")

cam.release()
cv2.destroyAllWindows()
