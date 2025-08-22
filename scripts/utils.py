import cv2

def create_fullscreen_window(window_name="Eye Mouse"):
    """Create a fullscreen OpenCV window."""
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
