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

jump_controller: Controller = Controller()


def dino3() -> None:
    def execute_jump(queue: Queue) -> None:
        def jump(controller: Controller) -> None:
            controller.press(Key.space)
            controller.release(Key.space)
            print('Jump')

        while True:
            # start_time: float = time()

            if queue.get() is True:
                jump(jump_controller)

            # print(f'execute_jump is %s seconds' % (time() - start_time))

    def find_jump_cases(queue: Queue, find_image: ndarray, x_min_distance: int) -> None:
        def make_screenshot(base_mss: MSSBase, grab_monitor: tuple[int, int, int, int]) -> ndarray:
            screenshot_array = array(base_mss.grab(grab_monitor))

            return cvtColor(screenshot_array, IMREAD_COLOR)

        def is_need_to_jump(need_to_jump_screenshot: ndarray) -> bool:
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

            def is_close_to_dino(close_image: ndarray, close_screenshot: ndarray, x_min: int) -> bool:
                result: ndarray = match_all(close_image, close_screenshot) > SUCCESSFUL_MATCHED_PERCENT
                y_result, x_result = where(result > SUCCESSFUL_MATCHED_PERCENT)

                if y_result.any() and x_result.any():
                    x: int = max(x_result)
                    # y: int = max(y_result)

                    return x - dino_x < x_min

                return False

            dino = get_dino(need_to_jump_screenshot)

            if dino is None:
                return False

            dino_x, dino_y = dino

            return is_close_to_dino(find_image, need_to_jump_screenshot, x_min_distance)

        monitor: tuple[int, int, int, int] = (0, 0, 1920, 1080)
        base: MSSBase = mss()

        while True:
            # start_time: float = time()
            jump_screenshot: ndarray = make_screenshot(base, monitor)

            if is_need_to_jump(jump_screenshot):
                queue.put(True)
                queue.task_done()

            # print(f'find_jump_cases is %s seconds' % (time() - start_time))

    dino_queue: Queue = Queue()

    execute_jump_thread: Thread = Thread(target=execute_jump, daemon=False, args=(dino_queue,))
    big_catus_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, BIG_CACTUS_IMAGE, 400))
    catus_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, CACTUS_IMAGE, 450))
    pterodactyl_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, PTERODACTYL_IMAGE, 500))

    execute_jump_thread.start()
    big_catus_thread.start()
    catus_thread.start()
    pterodactyl_thread.start()

    dino_queue.join()

    execute_jump_thread.join()
    big_catus_thread.join()
    catus_thread.join()
    pterodactyl_thread.join()


if __name__ == '__main__':
    dino3()
