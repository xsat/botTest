from mss import mss
from numpy import ndarray, array
from cv2 import cvtColor, IMREAD_COLOR


def create_screenshot(left: int = 0, top: int = 0, width: int = 1920, height: int = 1080) -> ndarray:
    base = mss()
    monitor = (left, top, width, height)
    screenshot = base.grab(monitor)
    screenshot_array = array(screenshot)

    return cvtColor(screenshot_array, IMREAD_COLOR)


if __name__ == '__main__':
    print(create_screenshot())
