from create_screenshot import create_screenshot
from match_image import match_image, match_all
from numpy import ndarray, where
from pynput.keyboard import Controller, Key
from location import Location


DINO_IMAGE = '_dino.jpg'
CACTUS_IMAGE = '_cactus.jpg'
BAT_IMAGE = '_bat.jpg'
OBSTACLE_IMAGE = '_obstacle.jpg'
GAME_OVER_IMAGE = '_game_over.jpg'


CACTUS_SMALL_IMAGE = 1
CACTUS_LARGE_IMAGE = 1
OBSTACLE_1_IMAGE = 1
OBSTACLE_2_IMAGE = 1
PTERODACTYL_IMAGE = 1

SUCCESSFUL_MATCHED_PERCENT = .8


def dino_jump(dino_keyboard_controller: Controller) -> None:
    dino_keyboard_controller.press(Key.space)
    dino_keyboard_controller.release(Key.space)


def is_game_over(game_over_screenshot: ndarray) -> bool:
    _, game_over_matched_percent = match_image(GAME_OVER_IMAGE, game_over_screenshot)

    return game_over_matched_percent > SUCCESSFUL_MATCHED_PERCENT


def is_dino_need_to_jump(dino_need_to_jump_screenshot: ndarray, dino_need_to_jump_location: Location) -> bool:
    def is_need_to_jump(needed_image: str, need_to_jump_screenshot: ndarray, need_to_jump_location: Location) -> bool:
        def is_close_to_jump(dino_location: Location, catus_location: Location) -> bool:
            x_between: int = abs(dino_location.get_x() - catus_location.get_x())
            min_between: int = 300
            max_between: int = 50
            # print(x_between)

            return min_between > x_between > max_between

            # return min_between > x_between
    
        result: ndarray = match_all(needed_image, need_to_jump_screenshot)

        # for item in

        matched_result: ndarray = where(result > SUCCESSFUL_MATCHED_PERCENT)

        for x, y in zip(*matched_result[::-1]):
            if is_close_to_jump(need_to_jump_location, Location(x, y)):
                return True

        return False

    if is_need_to_jump(OBSTACLE_IMAGE, dino_need_to_jump_screenshot, dino_need_to_jump_location):
        return True

    # if is_need_to_jump(CACTUS_IMAGE, dino_need_to_jump_screenshot, dino_need_to_jump_location):
    #     return True
    #
    # if is_need_to_jump(BAT_IMAGE, dino_need_to_jump_screenshot, dino_need_to_jump_location):
    #     return True

    return False


def dino_bot() -> None:
    first_screenshot = create_screenshot()
    dino_location, dino_matched_percent = match_image(DINO_IMAGE, first_screenshot)
    # if dino_matched_percent > SUCCESSFUL_MATCHED_PERCENT:
    game_keyboard_controller = Controller()
    is_dino_run = True
    while is_dino_run:
        game_status_screenshot = create_screenshot()
        if is_game_over(game_status_screenshot):
            is_dino_run = False

            print('Game over')
        else:
            if is_dino_need_to_jump(game_status_screenshot, dino_location):
                dino_jump(game_keyboard_controller)


if __name__ == '__main__':
    dino_bot()
