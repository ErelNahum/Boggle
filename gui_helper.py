from typing import Tuple


class Misc:
    @staticmethod
    def add_coors(coor1 : Tuple[int, int], coor2: Tuple[int, int]) -> Tuple[int, int]:
        return coor1[0] + coor2[0], coor1[1] + coor2[1]
    
    @staticmethod
    def neighbors_in_board(coor):
        if not coor:
            return []
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                g = Misc.add_coors(coor, (delta_x, delta_y))
                if Game.in_board(g):
                    yield g

class Timer:
    def __init__(self):
        self.time = 180  # 3 minutes

    def dec(self):
        self.time -= 1

    @staticmethod
    def make_int_two_digits(i):
        s = str(i)
        return '0' * (2 - len(s)) + s

    def __str__(self):
        """returns the time is a format of 'MM:SS'."""
        minutes = self.time // 60
        seconds = self.time % 60

        minutes = Timer.make_int_two_digits(minutes)
        seconds = Timer.make_int_two_digits(seconds)

        return minutes+':'+seconds


class Game:
    @staticmethod
    def in_board(coordinate: Tuple[int, int]):
        x, y = coordinate
        return 0 <= x <= 3 and 0 <= y <= 3
