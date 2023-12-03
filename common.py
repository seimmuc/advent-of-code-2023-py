from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO
from typing import Iterator, Union


class Day(ABC):
    @abstractmethod
    def solve_part1(self, input_str: str) -> str:
        raise NotImplemented

    @abstractmethod
    def solve_part2(self, input_str: str) -> str:
        raise NotImplemented


def line_iterator(multiline_string: str, strip_newline: bool = True) -> Iterator[str]:
    for line in StringIO(multiline_string):
        if strip_newline:
            line = line.rstrip('\r\n')
        yield line


# 2D grids

class Direction(Enum):
    Up = (0, -1)
    Down = (0, 1)
    Left = (-1, 0)
    Right = (1, 0)
    UpLeft = (-1, -1)
    UpRight = (1, -1)
    DownLeft = (-1, 1)
    DownRight = (1, 1)


DIRECTIONS_ALL = [
    Direction.Up, Direction.UpRight, Direction.Right, Direction.DownRight, Direction.Down, Direction.DownLeft,
    Direction.Left, Direction.UpLeft
]
DIRECTIONS_CARDINAL = [Direction.Up, Direction.Down, Direction.Left, Direction.Right]
DIRECTIONS_ORDINAL = [Direction.UpLeft, Direction.UpRight, Direction.DownLeft, Direction.DownRight]


class Vector:
    __slots__ = ['x', 'y']

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    @staticmethod
    def from_direction(direction: Direction) -> 'Vector':
        return Vector(direction.value[0], direction.value[1])

    def move_in(self, direction: Direction, dist: int = 1):
        return self + Vector(direction.value[0] * dist, direction.value[1] * dist)

    def __add__(self, other: Union['Vector', Direction]) -> 'Vector':
        if isinstance(other, Direction):
            return self.move_in(other)
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vector') -> 'Vector':
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, multiplier: int) -> 'Vector':
        return Vector(self.x * multiplier, self.y * multiplier)

    def __repr__(self):
        return f'Vector({self.x}, {self.y})'

    def __eq__(self, other: 'Vector'):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))
