from typing import List, Iterator, Tuple

from common import Day, line_iterator, Vector, DIRECTIONS_ALL, Direction


DIGITS = set(str(i) for i in range(0, 10))


class Day3Grid:
    def __init__(self):
        self.lines: List[str] = []
        self._width: int = 0

    @property
    def height(self):
        return len(self.lines)

    @property
    def width(self):
        return self._width

    def add_line(self, line: str):
        if len(self.lines) < 1:
            self._width = len(line)
        elif len(line) != self._width:
            raise RuntimeError(f'width mismatch: {len(line)} != {self._width}')
        self.lines.append(line)

    def is_in_bounds(self, pos: Vector) -> bool:
        return 0 <= pos.x < self._width and 0 <= pos.y < len(self.lines)

    def get_cell(self, pos: Vector) -> str:
        if not self.is_in_bounds(pos):
            raise RuntimeError(f'pos {pos} is out of bounds')
        return self.lines[pos.y][pos.x]

    def look_around(self, pos: Vector) -> Iterator[Tuple[Vector, str]]:
        for d in DIRECTIONS_ALL:
            v = pos + d
            if self.is_in_bounds(v):
                yield v, self.get_cell(v)

    def full_scan(self) -> Iterator[Tuple[Vector, str]]:
        for y in range(self.height):
            for x in range(self.width):
                v = Vector(x, y)
                yield v, self.get_cell(v)


class Day3(Day):
    @staticmethod
    def parse_input(input_str: str) -> Day3Grid:
        grid = Day3Grid()
        for line in line_iterator(input_str):
            grid.add_line(line)
        return grid

    @staticmethod
    def scan_for_symbols(grid: Day3Grid):
        for vec, val in grid.full_scan():
            if val == '.' or val in DIGITS:
                continue
            yield vec, val

    @staticmethod
    def get_full_number(grid: Day3Grid, digit_vector: Vector) -> Tuple[int, List[Vector]]:
        # find leftmost digit
        v = digit_vector
        while v.x >= 0 and grid.get_cell(v) in DIGITS:
            v = v.move_in(Direction.Left)
        v = v.move_in(Direction.Right)
        # capture full number
        number = 0
        all_digits = []
        while v.x < grid.width:
            d = grid.get_cell(v)
            if d not in DIGITS:
                break
            number = number * 10 + int(d)
            all_digits.append(v)
            v = v.move_in(Direction.Right)
        return number, all_digits

    def solve_part1(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        result = 0
        known_digits: set[Vector] = set()
        for vec, val in self.scan_for_symbols(grid):
            for la_vec, la_val in grid.look_around(vec):
                if la_val in DIGITS and la_vec not in known_digits:
                    num, all_digit_cells = self.get_full_number(grid, la_vec)
                    result += num
                    known_digits.update(all_digit_cells)
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        grid = self.parse_input(input_str)
        result = 0
        for vec, val in self.scan_for_symbols(grid):
            if val != '*':
                continue
            known_digits: set[Vector] = set()
            numbers: list[int] = []
            for la_vec, la_val in grid.look_around(vec):
                if la_val in DIGITS and la_vec not in known_digits:
                    num, all_digit_cells = self.get_full_number(grid, la_vec)
                    numbers.append(num)
                    known_digits.update(all_digit_cells)
            if len(numbers) == 2:
                result += numbers[0] * numbers[1]
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=3, part=1, s_class=Day3)
    run_puzzle(day=3, part=2, s_class=Day3)
