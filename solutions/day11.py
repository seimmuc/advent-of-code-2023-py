from bisect import bisect_left
from itertools import combinations
from typing import Iterator, Tuple

from common import Day, line_iterator, Grid, Vector


class Galaxy:
    def __init__(self, gid: int, location: Vector = None):
        self.id = gid
        self.location: Vector | None = location

    def distance_to(self, other: 'Galaxy') -> int:
        pass


class GalaxyGrid(Grid[Galaxy | None]):
    pass

    # Unused methods

    # def insert_line(self, y: int, line: list[Galaxy | None]):
    #     if not 0 <= y <= self.height:
    #         raise RuntimeError(f'cannot insert line: out of bounds (y={y})')
    #     if len(line) != self.width:
    #         raise RuntimeError(f'cannot insert line: width mismatch ({len(line)} != {self.width})')
    #     self.lines.insert(y, line)

    # def insert_column(self, x: int, column: list[Galaxy | None]):
    #     if not 0 <= x <= self.width:
    #         raise RuntimeError(f'cannot insert column: out of bounds (x={x})')
    #     if len(column) != self.height:
    #         raise RuntimeError(f'cannot insert column: height mismatch ({len(column)} != {self.height})')
    #     for i, line in enumerate(self.lines):   # type: int, list[Galaxy | None]
    #         line.insert(x, column[i])
    #     self._width += 1


class Day11(Day):
    @staticmethod
    def parse_input(input_str: str) -> Tuple[GalaxyGrid, list[Galaxy]]:
        gid = 0
        grid = GalaxyGrid()
        galaxies: list[Galaxy] = []
        for y, line in enumerate(line_iterator(input_str)):
            galaxies_line = []
            for x, s in enumerate(line.strip()):
                if s == '.':
                    galaxies_line.append(None)
                else:
                    gid += 1
                    g = Galaxy(gid, Vector(x=x, y=y))
                    galaxies.append(g)
                    galaxies_line.append(g)
            grid.add_line(galaxies_line)
        return grid, galaxies

    @staticmethod
    def adjust_coordinates(grid: GalaxyGrid, galaxies: list[Galaxy], ex_fac: int):
        ex_fac -= 1
        empty_columns = sorted(x for x in range(grid.width) if not any(g is not None for _, g in grid.scan_column(x)))
        empty_rows = sorted(y for y in range(grid.height) if not any(g is not None for _, g in grid.scan_row(y)))
        for g in galaxies:
            g.location.x += ex_fac * bisect_left(a=empty_columns, x=g.location.x)
            g.location.y += ex_fac * bisect_left(a=empty_rows, x=g.location.y)

    @staticmethod
    def do_math(galaxies: list[Galaxy]) -> int:
        result = 0
        for g1, g2 in combinations(galaxies, r=2):  # type: Galaxy, Galaxy
            result += (g1.location - g2.location).manhattan_distance
        return result

    def solve_part1(self, input_str: str) -> str:
        grid, galaxies = self.parse_input(input_str)
        self.adjust_coordinates(grid=grid, galaxies=galaxies, ex_fac=2)
        return str(self.do_math(galaxies=galaxies))

    def solve_part2(self, input_str: str) -> str:
        grid, galaxies = self.parse_input(input_str)
        self.adjust_coordinates(grid=grid, galaxies=galaxies, ex_fac=1000000)
        return str(self.do_math(galaxies=galaxies))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=11, part=1, s_class=Day11, path_prefix='..')
    run_puzzle(day=11, part=2, s_class=Day11, path_prefix='..')
