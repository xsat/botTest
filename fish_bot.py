from create_screenshot import create_screenshot
from match_image import match_image, is_matched_image
from walk_to import walk_to


def fish_bot() -> None:
    screenshot = create_screenshot()
    matched_result = match_image('dock_place.jpg', screenshot)
    location, _ = matched_result

    if is_matched_image(matched_result):
        print(location.get_x(), location.get_y())
        walk_to(location, 3)
    else:
        print('No match')


if __name__ == '__main__':
    fish_bot()
