import pyautogui

# Disable PyAutoGUI failsafe
pyautogui.FAILSAFE = False

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
