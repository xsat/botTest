from pydirectinput import moveTo, mouseDown, mouseUp
from time import sleep
from random import random
from location import Location


def walk_to(location: Location, click_time: float | None = None) -> None:
    def get_random_click_time() -> float:
        return .4 + random()

    moveTo(location.get_x(), location.get_y())
    mouseDown()

    if click_time is None:
        click_time = get_random_click_time()

    sleep(click_time)
    mouseUp()


if __name__ == '__main__':
    walk_to(Location(10, 10))
