from mss import mss
from cv2 import cvtColor, IMREAD_COLOR
from cv2 import imread, matchTemplate, minMaxLoc, IMREAD_UNCHANGED, TM_CCOEFF_NORMED
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


def dino3() -> None:
    def execute_jump(queue: Queue) -> None:
        jump_controller: Controller = Controller()

        def jump(controller: Controller) -> None:
            controller.press(Key.space)
            controller.release(Key.space)
            # print('Jump')

        while True:
            # start_time: float = time()

            if queue.get() is True:
                jump(jump_controller)

            # print(f'execute_jump is %s seconds' % (time() - start_time))

    def find_jump_cases(queue: Queue, find_image: ndarray, image_name: str) -> None:
        def make_screenshot() -> ndarray:
            base = mss()
            monitor = (0, 0, 1920, 1080)
            screenshot = base.grab(monitor)
            screenshot_array = array(screenshot)

            return cvtColor(screenshot_array, IMREAD_COLOR)

        def is_need_to_jump(screenshot: ndarray, find_image: ndarray) -> bool:
            def match_all(image: ndarray, haystack: ndarray) -> ndarray:
                return matchTemplate(haystack, image, TM_CCOEFF_NORMED)

            def match_one(image: ndarray, haystack: ndarray) -> tuple[float, float, float]:
                result_try: ndarray = match_all(image, haystack)
                _, max_val, _, max_loc = minMaxLoc(result_try)
                max_x, max_y = max_loc

                return max_x, max_y, max_val

            def get_dino() -> tuple[float, float] | None:
                max_x, max_y, matched_percent = match_one(DINO_IMAGE, screenshot)
                if matched_percent > SUCCESSFUL_MATCHED_PERCENT:
                    return max_x, max_y

                return None

            def is_close_to_dino(image: ndarray) -> bool:
                result: ndarray = match_all(image, screenshot) > SUCCESSFUL_MATCHED_PERCENT
                matched_results: ndarray = where(result > SUCCESSFUL_MATCHED_PERCENT)

                for y, x in zip(*matched_results):
                    if x - dino_x < 400:
                        # print(f'x:{x} y:{y}')
                        # print(f'dino_x:{dino_x} dino_y:{dino_y}')

                        return True

                return False

            dino = get_dino()

            # print(dino)
            if dino is None:
                return False

            dino_x, dino_y = dino

            return is_close_to_dino(find_image)

        while True:
            # start_time: float = time()
            jump_screenshot: ndarray = make_screenshot()

            if is_need_to_jump(jump_screenshot, find_image):
                queue.put(True)
                queue.task_done()

            # print(f'find_jump_cases in {image_name} is %s seconds' % (time() - start_time))

    dino_queue: Queue = Queue()

    execute_jump_thread: Thread = Thread(target=execute_jump, daemon=False, args=(dino_queue,))
    big_catus_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, BIG_CACTUS_IMAGE, 'BIG_CACTUS'))
    catus_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, CACTUS_IMAGE, 'CACTUS'))
    pterodactyl_thread: Thread = Thread(target=find_jump_cases, daemon=True, args=(dino_queue, PTERODACTYL_IMAGE, 'PTERODACTYL'))

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

