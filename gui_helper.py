from typing import List, Tuple
from exceptions import UnvalidMove


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


class Node:
    def __init__(self, value=None, next=None):
        self.value = value
        self.next = next

    @staticmethod
    def list_to_node(p: List):
        if not p:
            return None
        return Node(p[0], Node.list_to_node(p[1:]))

    def to_list(self):
        if self.next is None:
            return []
        return [self.value] + self.next.to_list()


class Path:

    def __init__(self, data=None):
        if data is None:
            self.pointer = None
            self.length = 0
        else:
            self.pointer = Node.list_to_node(data)
            self.length = len(data)

    def choose_coor(self, coor):
        if coor not in self.neighbors_in_board():
            raise UnvalidMove
        self.pointer = Node(coor, self.pointer)

    def to_list(self):
        return self.pointer.to_list()

    def selected(self):
        return self.to_list()

    @property
    def last_coor(self):
        return self.pointer.value

    def neighbors_in_board(self):
        for delta_x in (-1, 0, 1):
            for delta_y in (-1, 0, 1):
                manipulation_coor = delta_x, delta_y
                coor = Misc.add_coors(self.last_coor, manipulation_coor)
                if Game.in_board(coor):
                    yield coor

    def possible_moves(self):
        return [coor for coor in self.neighbors_in_board() if coor not in self.to_list()]


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
    def __init__(self):
        self.__current_path = Path()

    @staticmethod
    def in_board(coordinate: Tuple[int, int]):
        x, y = coordinate
        return 0 <= x <= 3 and 0 <= y <= 3
