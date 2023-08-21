class Location:
    def __init__(self, x: int, y: int) -> None:
        self.__x = x
        self.__y = y

    def get_x(self) -> int:
        return self.__x

    def get_y(self) -> int:
        return self.__y

    __x: int
    __y: int


if __name__ == '__main__':
    test_location = Location(10, 10)
    print(test_location, test_location.get_x(), test_location.get_y())
