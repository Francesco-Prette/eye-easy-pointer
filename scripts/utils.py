import cv2

def create_fullscreen_window(window_name="Calibration"):
    """Create a fullscreen OpenCV window."""
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
