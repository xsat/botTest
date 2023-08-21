from cv2 import imread, matchTemplate, minMaxLoc, IMREAD_UNCHANGED, TM_CCOEFF_NORMED
from numpy import ndarray
from create_screenshot import create_screenshot
from location import Location


def match_image(filename: str, haystack: ndarray) -> tuple[Location, float]:
    box_img: ndarray = imread(filename, IMREAD_UNCHANGED)
    result_try: ndarray = matchTemplate(haystack, box_img, TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = minMaxLoc(result_try)
    max_x, max_y = max_loc

    return Location(max_x, max_y), max_val


def match_all(filename: str, haystack: ndarray) -> ndarray:
    img: ndarray = imread(filename, IMREAD_UNCHANGED)
    return matchTemplate(haystack, img, TM_CCOEFF_NORMED)
    # images = where(threshold > result_try)
    # matched_locations: list[Location] = []
    #
    # for x, y in zip(*images[::-1]):
    #     matched_locations.append(Location(x, y))
    #
    # return matched_locations


def is_matched_image(matched_result: tuple[Location, float], threshold: float = .8) -> bool:
    _, max_match_val = matched_result

    return max_match_val > threshold


if __name__ == '__main__':
    test_screenshot: ndarray = create_screenshot()
    print(match_image('ww.jpg', test_screenshot))
    print(match_image('w.jpg', test_screenshot))
