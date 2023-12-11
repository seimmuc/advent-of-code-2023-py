from typing import Tuple, Literal, Iterable, Sequence, Iterator

from common import Day, Vector, Direction, DIRECTIONS_CARDINAL, line_iterator, Grid, GT


PipeMapMark = Literal['|', '-', 'L', 'J', '7', 'F', '.', 'S']


PIPE_TYPE_LEGEND: dict[PipeMapMark, Tuple[Direction, ...]] = {
    '|': (Direction.Up, Direction.Down),
    '-': (Direction.Left, Direction.Right),
    'L': (Direction.Up, Direction.Right),
    'J': (Direction.Up, Direction.Left),
    '7': (Direction.Down, Direction.Left),
    'F': (Direction.Down, Direction.Right),
    '.': tuple(),
    'S': (Direction.Up, Direction.Right, Direction.Down, Direction.Left),
}
PIPE_TYPE_SIDES: dict[PipeMapMark, dict[Direction: Sequence[Direction]]] = {
    '|': {
        Direction.Up: (Direction.UpRight, Direction.Right, Direction.DownRight),
        Direction.Down: (Direction.UpLeft, Direction.Left, Direction.DownLeft)
    },
    '-': {
        Direction.Left: (Direction.UpLeft, Direction.Up, Direction.UpRight),
        Direction.Right: (Direction.DownLeft, Direction.Down, Direction.DownRight)
    },
    'L': {
        Direction.Down: (Direction.DownRight, Direction.Down, Direction.DownLeft, Direction.Left, Direction.UpLeft),
        Direction.Left: (Direction.UpRight,)
    },
    'J': {
        Direction.Down: (Direction.UpLeft,),
        Direction.Right: (Direction.DownLeft, Direction.Down, Direction.DownRight, Direction.Right, Direction.UpRight)
    },
    '7': {
        Direction.Up: (Direction.UpLeft, Direction.Up, Direction.UpRight, Direction.Right, Direction.DownRight),
        Direction.Right: (Direction.DownLeft,)
    },
    'F': {
        Direction.Up: (Direction.DownRight,),
        Direction.Left: (Direction.UpRight, Direction.Up, Direction.UpLeft, Direction.Left, Direction.DownLeft)
    },
}


class PipeTile:
    def __init__(self, pos: Vector, pipe_type: PipeMapMark):
        self.pos = pos
        self.pipe_type = pipe_type

    def connects_to(self, d: Direction):
        if self.pipe_type == 'S':
            return d in DIRECTIONS_CARDINAL
        else:
            return d in PIPE_TYPE_LEGEND[self.pipe_type]


class PipeMap(Grid[PipeMapMark]):
    def add_line(self, line: str):
        return super().add_line(line)

    def get_connections(self, pos: Vector) -> Iterable[Direction]:
        p = self.get_cell(pos)
        if p == '.':
            return tuple()
        if p == 'S':
            return DIRECTIONS_CARDINAL
        return PIPE_TYPE_LEGEND[p]

    def get_verified_connected_tiles(self, pos: Vector, ignore: Vector = None) -> Iterator[Tuple[Direction, Vector]]:
        for d in self.get_connections(pos):
            p = pos + d
            if p != ignore and self.is_in_bounds(p) and d.inverse in self.get_connections(p):
                yield d, p


class OutOfBoundsError(RuntimeError):
    pass


class Day10(Day):
    @staticmethod
    def parse_input(input_str: str) -> Tuple[PipeMap, Vector]:
        pipe_map = PipeMap()
        start_pos: Vector | None = None
        for y, line in enumerate(line_iterator(input_str)):
            pipe_map.add_line(line.strip())
            if 'S' in line:
                for x in (i for i, c in enumerate(line) if c == 'S'):
                    if start_pos is not None:
                        raise RuntimeError('multiple starting positions found')
                    start_pos = Vector(x, y)
        if start_pos is None:
            raise RuntimeError('no starting position found')
        return pipe_map, start_pos

    @staticmethod
    def walk_loop(pipe_map: PipeMap, start_pos: Vector, start_direction: Direction)\
            -> Iterator[Tuple[Direction, Vector]]:
        if start_direction not in (d for d, p in pipe_map.get_verified_connected_tiles(pos=start_pos)):
            raise RuntimeError('cannot walk loop: no pipe connection in given direction')
        cur_pos = start_pos + start_direction
        prev_pos = start_pos
        yield start_direction, cur_pos
        while True:
            next_steps = list(pipe_map.get_verified_connected_tiles(pos=cur_pos, ignore=prev_pos))
            if len(next_steps) != 1:
                raise RuntimeError('something went very wrong')
            prev_pos = cur_pos
            cur_pos = next_steps[0][1]
            if cur_pos == start_pos:
                return
            yield next_steps[0][0], cur_pos

    @staticmethod
    def iter_area(pipe_map: PipeMap, start: Vector, boundaries: set[Vector], ignore: set[Vector], oob: set[Vector],
                  out_of_bounds_err=True) -> Iterator[Vector]:
        loose_ends = [start]
        found = set()
        while loose_ends:
            c_pos = loose_ends.pop()
            if c_pos in boundaries or c_pos in ignore or c_pos in found:
                continue
            if c_pos in oob or not pipe_map.is_in_bounds(c_pos):
                if out_of_bounds_err:
                    raise OutOfBoundsError()
                continue
            yield c_pos
            found.add(c_pos)
            loose_ends.extend(c_pos + d for d in DIRECTIONS_CARDINAL)

    def solve_part1(self, input_str: str) -> str:
        pipe_map, start_pos = self.parse_input(input_str)
        start_connections = list(pipe_map.get_verified_connected_tiles(pos=start_pos))
        if len(start_connections) != 2:
            raise RuntimeError('start has more than 2 connections!')
        loop_tiles: dict[Vector, int] = {start_pos: 0}
        for sd, _ in start_connections:
            cur_dist = 1
            for _, pos in self.walk_loop(pipe_map=pipe_map, start_pos=start_pos, start_direction=sd):
                if pos not in loop_tiles or loop_tiles[pos] > cur_dist:
                    loop_tiles[pos] = cur_dist
                cur_dist += 1
        return str(max(loop_tiles.values()))

    def solve_part2(self, input_str: str) -> str:
        pipe_map, start_pos = self.parse_input(input_str)
        start_directions = list(sd for sd, _ in pipe_map.get_verified_connected_tiles(pos=start_pos))
        loop_tiles: set[Vector] = {start_pos}
        loop_tiles.update(p for d, p in self.walk_loop(pipe_map=pipe_map, start_pos=start_pos,
                                                       start_direction=start_directions[0]))

        inner_tiles: set[Vector] | None = None
        for sd in start_directions:
            try:
                it: set[Vector] = set()
                for d, p in self.walk_loop(pipe_map=pipe_map, start_pos=start_pos, start_direction=sd):
                    tile = pipe_map.get_cell(p)
                    for td in PIPE_TYPE_SIDES[tile][d]:
                        for v in self.iter_area(pipe_map, p + td, loop_tiles, it, set()):
                            it.add(v)
                    pass
                inner_tiles = it
                break
            except OutOfBoundsError:
                continue
        if inner_tiles is None:
            raise RuntimeError('somehow neither side encloses an area')

        # def ch(v: Vector):
        #     if v in inner_tiles and v in loop_tiles:
        #         raise RuntimeError()
        #     if v in loop_tiles:
        #         return pipe_map.get_cell(v)
        #     if v in inner_tiles:
        #         return '!'
        #     return '.'
        #
        # new_pipe_map = PipeMap()
        # for y, pm_line in enumerate(pipe_map.lines):
        #     new_line = ''.join(ch(Vector(x, y)) for x, c in enumerate(pm_line))
        #     new_pipe_map.add_line(new_line)
        # for npl in new_pipe_map.lines:
        #     print(npl)

        return str(len(inner_tiles))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=10, part=1, s_class=Day10, path_prefix='..')
    run_puzzle(day=10, part=2, s_class=Day10, path_prefix='..')
