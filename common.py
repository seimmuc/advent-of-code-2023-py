from abc import ABC, abstractmethod
from enum import Enum
from io import StringIO
from typing import Iterator, Union, Iterable, Generic, TypeVar, Sequence, Tuple


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


def batch_iterator(iterable: Iterable, n: int, allow_incomplete_batch: bool = True):
    # python 3.12 has itertools.batched(), but I'm still using 3.10 :(
    iterable = iter(iterable)
    batch = []
    while True:
        try:
            batch.append(next(iterable))
        except StopIteration:
            if len(batch) < 1:
                return
            elif allow_incomplete_batch:
                yield tuple(batch)
                return
            raise
        if len(batch) == n:
            yield tuple(batch)
            batch.clear()


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
    
    @property
    def inverse(self) -> 'Direction':
        return DIRECTIONS_INVERSES.get(self)


DIRECTIONS_ALL = (
    Direction.Up, Direction.UpRight, Direction.Right, Direction.DownRight, Direction.Down, Direction.DownLeft,
    Direction.Left, Direction.UpLeft
)
DIRECTIONS_CARDINAL = (Direction.Up, Direction.Down, Direction.Left, Direction.Right)
DIRECTIONS_ORDINAL = (Direction.UpLeft, Direction.UpRight, Direction.DownLeft, Direction.DownRight)
DIRECTIONS_INVERSES: dict[Direction, Direction] = {d: next(di for di in DIRECTIONS_ALL
                                                           if di.value[0] == 0 - d.value[0]
                                                           and di.value[1] == 0 - d.value[1])
                                                   for d in DIRECTIONS_ALL}
DIRECTION_TURN_CARDINAL = {
    Direction.Up: {'right': Direction.Right, 'left': Direction.Left, 'around': Direction.Down},
    Direction.Right: {'right': Direction.Down, 'left': Direction.Up, 'around': Direction.Left},
    Direction.Down: {'right': Direction.Left, 'left': Direction.Right, 'around': Direction.Up},
    Direction.Left: {'right': Direction.Up, 'left': Direction.Down, 'around': Direction.Right}
}


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
    
    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)

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
        return other is not None and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


GT = TypeVar('GT')


class Grid(Generic[GT]):
    def __init__(self):
        self.lines: list[Sequence[GT]] = []
        self._width: int = 0

    @property
    def height(self):
        return len(self.lines)

    @property
    def width(self):
        return self._width

    def add_line(self, line: Sequence[GT]):
        if len(self.lines) < 1:
            self._width = len(line)
        elif len(line) != self._width:
            raise RuntimeError(f'cannot add line to grid: width mismatch ({len(line)} != {self._width})')
        # noinspection PyTypeChecker
        self.lines.append(line)

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x < self._width and 0 <= pos.y < len(self.lines)

    def get_cell(self, pos: Vector) -> GT:
        if not self.is_in_bounds(pos):
            raise RuntimeError(f"pos {pos} is out of grid's bounds")
        return self.lines[pos.y][pos.x]

    def set_cell(self, pos: Vector, val: GT):
        if not self.is_in_bounds(pos):
            raise RuntimeError(f"pos {pos} is out of grid's bounds")
        self.lines[pos.y][pos.x] = val

    def look_around(self, pos: Vector, directions: Iterator[Direction] = DIRECTIONS_ALL) -> Iterator[Tuple[Vector, GT]]:
        for d in directions:
            v = pos + d
            if self.is_in_bounds(v):
                yield v, self.get_cell(v)

    def scan_row(self, y: int) -> Iterator[Tuple[Vector, GT]]:
        for x in range(self.width):
            v = Vector(x, y)
            yield v, self.get_cell(v)

    def scan_column(self, x: int) -> Iterator[Tuple[Vector, GT]]:
        for y in range(self.height):
            v = Vector(x, y)
            yield v, self.get_cell(v)

    def scan_all(self) -> Iterator[Tuple[Vector, GT]]:
        for y in range(self.height):
            for x in range(self.width):
                v = Vector(x, y)
                yield v, self.get_cell(v)
