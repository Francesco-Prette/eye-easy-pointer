import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import keyboard

# Turn of fail safe
pyautogui.FAILSAFE = False

# Screen size
screen_w, screen_h = pyautogui.size()

# Mediapipe FaceMesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Camera
cam = cv2.VideoCapture(0)

# Calibration data
calibration_points_screen = [
    (0, 0),  # top-left
    (screen_w, 0),  # top-right
    (0, screen_h),  # bottom-left
    (screen_w, screen_h),  # bottom-right
    (screen_w // 2, screen_h // 2)  # center
]
calibration_points_eye = []
calibrated = False
current_calibration_idx = 0

print("Calibration started: look at the red dot when shown")
print("Press SPACE to calibrate a point, ESC to exit, or SHIFT+ESC to force stop")

while True:
    # 🔴 FORCE STOP
    if keyboard.is_pressed("shift+esc"):
        print("Force stop triggered!")
        break

    ret, frame = cam.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)  # mirror for natural movement
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    h, w, _ = frame.shape

    # Show calibration dot
    if not calibrated and current_calibration_idx < len(calibration_points_screen):
        # Black fullscreen background
        calib_screen = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)

        # Red calibration dot
        cx, cy = calibration_points_screen[current_calibration_idx]
        cv2.circle(calib_screen, (cx, cy), 20, (0, 0, 255), -1)

        cv2.putText(calib_screen, "Look at the dot & press SPACE",
                    (50, 80), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

        # SHOW ONLY calibration screen
        cv2.imshow("Eye Mouse", calib_screen)

    if results.multi_face_landmarks:
        landmarks = results.multi_face_landmarks[0].landmark

        # Use right eye iris landmark
        right_eye = [
            landmarks[474].x * w,
            landmarks[474].y * h
        ]

        if not calibrated:
            cv2.putText(frame, "Press SPACE when looking at red dot", (30, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
            # Apply affine mapping
            eye_points = np.array(calibration_points_eye)
            screen_points = np.array(calibration_points_screen)

            M, _ = cv2.estimateAffine2D(eye_points, screen_points)
            if M is not None:
                eye_coords = np.array([[right_eye[0], right_eye[1]]])
                mapped = cv2.transform(np.array([eye_coords]), M)[0][0]

                pyautogui.moveTo(mapped[0], mapped[1])

    cv2.imshow("Eye Mouse", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC to quit normally
        break
    elif key == 32 and not calibrated:  # SPACE for calibration
        if results.multi_face_landmarks:
            landmarks = results.multi_face_landmarks[0].landmark
            eye = [landmarks[474].x * w, landmarks[474].y * h]
            calibration_points_eye.append(eye)
            current_calibration_idx += 1
            if current_calibration_idx >= len(calibration_points_screen):
                calibrated = True
                print("Calibration complete!")

cam.release()
cv2.destroyAllWindows()
