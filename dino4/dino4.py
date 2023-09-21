from mss import mss
from mss.base import MSSBase
from cv2 import imread, matchTemplate, minMaxLoc, cvtColor, IMREAD_UNCHANGED, TM_CCOEFF_NORMED, IMREAD_COLOR
from numpy import ndarray, array, where
from pynput.keyboard import Controller, Key
from threading import Thread
from queue import Queue
from time import time


BIG_CACTUS_IMAGE: ndarray = imread('_big_cactus.jpg', IMREAD_UNCHANGED)
CACTUS_IMAGE: ndarray = imread('_cactus.jpg', IMREAD_UNCHANGED)
PTERODACTYL_IMAGE: ndarray = imread('_pterodactyl.jpg', IMREAD_UNCHANGED)
DINO_IMAGE: ndarray = imread('_dino.jpg', IMREAD_UNCHANGED)

SUCCESSFUL_MATCHED_PERCENT: float = .8


def match_all(all_image: ndarray, all_haystack: ndarray) -> ndarray:
    return matchTemplate(all_haystack, all_image, TM_CCOEFF_NORMED)


def match_one(one_image: ndarray, one_haystack: ndarray) -> tuple[float, float, float]:
    result_try: ndarray = match_all(one_image, one_haystack)
    _, max_val, _, max_loc = minMaxLoc(result_try)
    max_x, max_y = max_loc

    return max_x, max_y, max_val


def get_dino(dino_screenshot: ndarray) -> tuple[float, float] | None:
    max_x, max_y, matched_percent = match_one(DINO_IMAGE, dino_screenshot)
    if matched_percent > SUCCESSFUL_MATCHED_PERCENT:
        return max_x, max_y

    return None


def get_close_to_dino(close_image: ndarray, close_screenshot: ndarray) -> tuple[int, int] | None:
    result: ndarray = match_all(close_image, close_screenshot) > SUCCESSFUL_MATCHED_PERCENT
    y_result, x_result = where(result > SUCCESSFUL_MATCHED_PERCENT)

    if y_result.any() and x_result.any():
        x: int = min(x_result)
        y: int = min(y_result)

        return x, y

    return None


def is_need_to_jump(need_to_jump_image: ndarray, need_to_jump_screenshot: ndarray, x_min_distance: int) -> bool:
    dino = get_dino(need_to_jump_screenshot)
    if dino is None:
        print('No dino')

        return False

    close_to_dino = get_close_to_dino(need_to_jump_image, need_to_jump_screenshot)
    if close_to_dino is None:
        print('No close_to_dino')

        return False

    dino_x, dino_y = dino
    x, y = close_to_dino

    print(f'x: {x}, y: {y}')
    print(f'dino_x: {dino_x}, dino_y: {dino_y}')
    print(f'x - dino_x: {x - dino_x}')

    return x - dino_x < x_min_distance


def dino4() -> None:
    print(is_need_to_jump(CACTUS_IMAGE, imread('img_0.png'), 150))
    print(is_need_to_jump(BIG_CACTUS_IMAGE, imread('img_1.png'), 300))
    print(is_need_to_jump(CACTUS_IMAGE, imread('img_2.png'), 150))
    print(is_need_to_jump(BIG_CACTUS_IMAGE, imread('img_3.png'), 300))
    print(is_need_to_jump(CACTUS_IMAGE, imread('img_4.png'), 150))

    pass


if __name__ == '__main__':
    dino4()