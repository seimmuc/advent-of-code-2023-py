import re
from typing import NamedTuple, Iterator

from common import Day, Direction, line_iterator, LGrid, Vector, DIRECTION_TURN_CARDINAL, Grid, DIRECTIONS_CARDINAL


DIR_MAP = {'U': Direction.Up, 'R': Direction.Right, 'D': Direction.Down, 'L': Direction.Left}
instruction_regex = re.compile(r'([A-Z]) (\d+) \(#[\da-f]{6}\)')


class DigInstruction(NamedTuple):
    direction: Direction
    distance: int


class DigMap(LGrid[bool]):
    pass


class OutOfBoundsError(RuntimeError):
    pass


class Day18(Day):
    @staticmethod
    def parse_input(input_str: str) -> list[DigInstruction]:
        instructions = []
        for line in line_iterator(input_str):
            match = instruction_regex.fullmatch(line.strip())
            instructions.append(DigInstruction(DIR_MAP[match[1]], int(match[2])))
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

    @classmethod
    def build_trench_map(cls, instructions: list[DigInstruction]) -> tuple[DigMap, Vector, set[Vector]]:
        min_x, max_x, min_y, max_y = 0, 0, 0, 0
        for v, _ in cls.iter_instructions(instructions, corners_only=True):
            min_x = min(min_x, v.x)
            max_x = max(max_x, v.x)
            min_y = min(min_y, v.y)
            max_y = max(max_y, v.y)
        dig_map = DigMap()
        for y in range(max_y + 1 - min_y):
            dig_map.add_line([False for _ in range(max_x + 1 - min_x)])
        start = Vector(-min_x, -min_y)
        trench_tiles: set[Vector] = set()
        for v, instr in cls.iter_instructions(instructions, start):
            dig_map.set_cell(v, True)
            trench_tiles.add(v)
        return dig_map, start, trench_tiles

    @staticmethod
    def iter_area(bounds_grid: Grid, start: Vector, boundaries: set[Vector], ignore: set[Vector],
                  out_of_bounds_err=True) -> Iterator[Vector]:
        loose_ends = [start]
        found = set()
        while loose_ends:
            c_pos = loose_ends.pop()
            if c_pos in boundaries or c_pos in ignore or c_pos in found:
                continue
            if not bounds_grid.is_in_bounds(c_pos):
                if out_of_bounds_err:
                    raise OutOfBoundsError()
                continue
            yield c_pos
            found.add(c_pos)
            loose_ends.extend(c_pos + d for d in DIRECTIONS_CARDINAL)

    def solve_part1(self, input_str: str) -> str:
        instructions = self.parse_input(input_str)
        dig_map, start_loc, trench_tiles = self.build_trench_map(instructions)
        inside_tiles: set[Vector] | None = None
        for side in ('right', 'left'):
            try:
                its: set[Vector] = set()
                for trench_vec, instr in self.iter_instructions(instructions, start=start_loc):
                    t = trench_vec + DIRECTION_TURN_CARDINAL[instr.direction][side]
                    for v in self.iter_area(dig_map, start=t, boundaries=trench_tiles, ignore=its):
                        its.add(v)
                inside_tiles = its
                break
            except OutOfBoundsError:
                continue
        if inside_tiles is None:
            raise RuntimeError()

        # print_map: LGrid[str] = LGrid()
        # for ln in dig_map.lines:
        #     print_map.add_line(list('#' if t else '.' for t in ln))
        # print_map.set_cell(start_loc, '@')
        # for it in inside_tiles:
        #     print_map.set_cell(it, '!')
        # for ln in print_map.lines:
        #     print(''.join(ln))
        return str(len(inside_tiles) + len(trench_tiles))

    def solve_part2(self, input_str: str) -> str:
        return None


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=18, part=1, s_class=Day18, path_prefix='..')
    run_puzzle(day=18, part=2, s_class=Day18, path_prefix='..')
