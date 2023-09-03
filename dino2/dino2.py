from mss import mss
from cv2 import cvtColor, IMREAD_COLOR
from cv2 import imread, matchTemplate, minMaxLoc, IMREAD_UNCHANGED, TM_CCOEFF_NORMED
from numpy import ndarray, array, where
from pynput.keyboard import Controller, Key

GAME_OVER_IMAGE: ndarray = imread('_game_over.jpg', IMREAD_UNCHANGED)
GAME_SCORE_IMAGE: ndarray = imread('_game_score.jpg', IMREAD_UNCHANGED)
BIG_CACTUS_IMAGE: ndarray = imread('_big_cactus.jpg', IMREAD_UNCHANGED)
CACTUS_IMAGE: ndarray = imread('_cactus.jpg', IMREAD_UNCHANGED)
PTERODACTYL_IMAGE: ndarray = imread('_pterodactyl.jpg', IMREAD_UNCHANGED)
DINO_IMAGE: ndarray = imread('_dino.jpg', IMREAD_UNCHANGED)


SUCCESSFUL_MATCHED_PERCENT: float = .8


def match_all(image: ndarray, haystack: ndarray) -> ndarray:
    # img: ndarray = imread(filename, IMREAD_UNCHANGED)

    return matchTemplate(haystack, image, TM_CCOEFF_NORMED)


def match_one(image: ndarray, haystack: ndarray) -> tuple[float, float, float]:
    result_try: ndarray = match_all(image, haystack)
    _, max_val, _, max_loc = minMaxLoc(result_try)
    max_x, max_y = max_loc

    return max_x, max_y, max_val


def make_screenshot() -> ndarray:
    base = mss()
    monitor = (0, 0, 1920, 1080)
    screenshot = base.grab(monitor)
    screenshot_array = array(screenshot)

    return cvtColor(screenshot_array, IMREAD_COLOR)


def is_game_over(screenshot: ndarray) -> bool:
    _, _, matched_percent = match_one(GAME_OVER_IMAGE, screenshot)

    return matched_percent > SUCCESSFUL_MATCHED_PERCENT


def is_game_going(screenshot: ndarray) -> bool:
    _, _, matched_percent = match_one(GAME_SCORE_IMAGE, screenshot)

    return matched_percent > SUCCESSFUL_MATCHED_PERCENT


def is_need_to_jump(screenshot: ndarray) -> bool:
    def get_dino() -> tuple[float, float] | None:
        max_x, max_y, matched_percent = match_one(DINO_IMAGE, screenshot)
        if matched_percent > SUCCESSFUL_MATCHED_PERCENT:
            return max_x, max_y

        return None

    def is_close_to_dino(image: ndarray) -> bool:
        result: ndarray = match_all(image, screenshot) > SUCCESSFUL_MATCHED_PERCENT
        matched_results: ndarray = where(result > SUCCESSFUL_MATCHED_PERCENT)

        for y, x in zip(*matched_results):
            print(f'x:{x} y:{y}')
            print(f'dino_x:{dino_x}dino_y:{dino_y}')

            if x - dino_x < 500:
                return True

        return False

    dino = get_dino()
    if dino is not None:
        dino_x, dino_y = dino

        if is_close_to_dino(CACTUS_IMAGE):
            return True

        if is_close_to_dino(BIG_CACTUS_IMAGE):
            return True

        if is_close_to_dino(PTERODACTYL_IMAGE):
            return True

    return False


def jump(controller: Controller) -> None:
    controller.press(Key.space)
    # sleep(.01)
    controller.release(Key.space)
    print('Jump')


def dino2() -> None:
    game_controller = Controller()

    while True:
        window_screenshot = make_screenshot()
        if is_game_over(window_screenshot):
            break

        if is_game_going(window_screenshot):
            print('game_going')
            if is_need_to_jump(window_screenshot):
                jump(game_controller)


if __name__ == '__main__':
    dino2()
