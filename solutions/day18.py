import re
from typing import NamedTuple, Iterator, Callable, Literal

from common import Day, Direction, line_iterator, LGrid, Vector, DIRECTION_TURN_CARDINAL, Grid, DIRECTIONS_CARDINAL


DIR_MAP = {
    'U': Direction.Up, 'D': Direction.Down, 'L': Direction.Left, 'R': Direction.Right,
    '0': Direction.Right, '1': Direction.Down, '2': Direction.Left, '3': Direction.Up
}
instruction_d1_regex = re.compile(r'([A-Z]) (\d+) \(#[\da-f]{6}\)')
instruction_d2_regex = re.compile(r'[A-Z] \d+ \(#([\da-f]{5})([0-3])\)')


class DigInstruction(NamedTuple):
    direction: Direction
    distance: int


# class DigMap(LGrid[bool]):
#     pass


# class OutOfBoundsError(RuntimeError):
#     pass


class Day18(Day):
    @staticmethod
    def parse_input(input_str: str, regex: re.Pattern, line_parser: Callable[[re.Match], tuple[Direction, int]])\
            -> list[DigInstruction]:
        instructions = []
        for line in line_iterator(input_str):
            match = regex.fullmatch(line.strip())
            direction, distance = line_parser(match)
            instructions.append(DigInstruction(direction, distance))
        return instructions

    @staticmethod
    def iter_instructions(instructions: list[DigInstruction], start=Vector(0, 0), corners_only=False)\
            -> Iterator[tuple[Vector, DigInstruction]]:
        v = start
        for instr in instructions:
            i_end = v.move_in(instr.direction, instr.distance)
            if corners_only:
                v = i_end
                yield v, instr
            else:
                while v != i_end:
                    v = v.move_in(instr.direction)
                    yield v, instr

    @staticmethod
    def clockwise(v: Vector, d: Direction) -> bool:
        return (v.x < 0) == (d == Direction.Up) if d.only_vertical else (v.y < 0) == (d == Direction.Right)

    @classmethod
    def do_math(cls, instructions: list[DigInstruction]) -> int:
        center = Vector(0, 0)
        instr_iter = cls.iter_instructions(instructions, corners_only=True)
        prev_corner, instr = next(instr_iter)
        area_outer_trench = 1 + instr.distance / 2
        area_inside = 0
        for vec, instr in instr_iter:
            area = (instr.distance * (abs(vec.x) if instr.direction.only_vertical else abs(vec.y))) / 2
            if cls.clockwise(prev_corner, instr.direction):
                area_inside += area
            else:
                area_inside -= area
            area_outer_trench += instr.distance / 2
            prev_corner = vec
        if prev_corner != center:
            raise RuntimeError("trench didn't make a loop")
        total_area = area_outer_trench + abs(area_inside)
        if total_area % 1 != 0:
            raise RuntimeError(f'total_area , which is not an integer')
        return int(total_area)

    def solve_part1(self, input_str: str) -> str:
        instructions = self.parse_input(input_str, instruction_d1_regex, lambda m: (DIR_MAP[m[1]], int(m[2])))
        return str(self.do_math(instructions))

    def solve_part2(self, input_str: str) -> str:
        instructions = self.parse_input(input_str, instruction_d2_regex, lambda m: (DIR_MAP[m[2]], int(m[1], 16)))
        return str(self.do_math(instructions))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=18, part=1, s_class=Day18, path_prefix='..')
    run_puzzle(day=18, part=2, s_class=Day18, path_prefix='..')
