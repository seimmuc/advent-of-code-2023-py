from abc import ABC, abstractmethod
from typing import Callable, Iterator, Sequence

from common import Day, Grid, Vector, Direction, line_iterator


class LightBeam:
    __slots__ = ['loc', 'dir']

    def __init__(self, location: Vector, direction: Direction):
        self.loc = location
        self.dir = direction


class LightContraptionTile(ABC):
    __slots__ = ['location', 'energised_dirs']

    def __init__(self, loc: Vector):
        self.location = loc
        self.energised_dirs: list[Direction] = []

    @abstractmethod
    def beam_hit(self, beam: LightBeam, add_beam: Callable[[LightBeam], None]):
        raise NotImplemented

    @classmethod
    def create(cls, loc: Vector, tile_type: str) -> 'LightContraptionTile':
        if tile_type == '.':
            return LCTileEmpty(loc=loc)
        if tile_type in '/\\':
            return LCTileMirror(loc=loc, tile_type=tile_type)
        if tile_type in '-|':
            return LCTileSplitter(loc=loc, tile_type=tile_type)


class LCTileEmpty(LightContraptionTile):
    __slots__ = []

    def beam_hit(self, beam: LightBeam, add_beam: Callable[[LightBeam], None]):
        beam.loc += beam.dir


class LCTileMirror(LightContraptionTile):
    RDS = [
        {
            Direction.Up: Direction.Right,
            Direction.Right: Direction.Up,
            Direction.Down: Direction.Left,
            Direction.Left: Direction.Down
        }, {
            Direction.Up: Direction.Left,
            Direction.Right: Direction.Down,
            Direction.Down: Direction.Right,
            Direction.Left: Direction.Up
        }
    ]
    __slots__ = ['vr']

    def __init__(self, loc: Vector, tile_type: str):
        super().__init__(loc)
        self.vr = 0 if tile_type == '/' else 1

    def beam_hit(self, beam: LightBeam, add_beam: Callable[[LightBeam], None]):
        beam.dir = self.RDS[self.vr][beam.dir]
        beam.loc += beam.dir


class LCTileSplitter(LightContraptionTile):
    SDS = [
        (Direction.Up, Direction.Down),
        (Direction.Right, Direction.Left)
    ]
    __slots__ = ['v']

    def __init__(self, loc: Vector, tile_type: str):
        super().__init__(loc)
        self.v = 0 if tile_type == '|' else 1

    def beam_hit(self, beam: LightBeam, add_beam: Callable[[LightBeam], None]):
        sd = self.SDS[self.v]
        if beam.dir in sd:
            beam.loc += beam.dir
        else:
            add_beam(LightBeam(beam.loc + sd[1], sd[1]))
            beam.dir = sd[0]
            beam.loc += sd[0]


class LightContraption(Grid[LightContraptionTile]):
    def __init__(self):
        super().__init__()
        self.all_tiles: list[LightContraptionTile] = []

    def add_line(self, line: Sequence[LightContraptionTile]):
        super().add_line(line)
        self.all_tiles.extend(line)

    def calc_energised_tiles_and_reset(self) -> int:
        et = 0
        for t in self.all_tiles:
            if t.energised_dirs:
                et += 1
                t.energised_dirs = []
        return et


class Day16(Day):
    @staticmethod
    def parse_input(input_str: str) -> LightContraption:
        contraption = LightContraption()
        for y, line in enumerate(line_iterator(input_str)):
            contraption.add_line([LightContraptionTile.create(Vector(x, y), s) for x, s in enumerate(line)])
        return contraption

    @staticmethod
    def simulate(contraption: LightContraption, beams: list[LightBeam]):
        add = beams.append
        while beams:
            b = beams[-1]
            if not contraption.is_in_bounds(b.loc):
                # beam went outside
                beams.pop()
                continue
            t = contraption.get_cell(b.loc)
            if b.dir in t.energised_dirs:
                # beam merges with one that was previously simulated
                beams.pop()
                continue
            t.energised_dirs.append(b.dir)
            t.beam_hit(b, add)

    @staticmethod
    def iter_edge_with_dirs(contraption: LightContraption) -> Iterator[tuple[Vector, Direction]]:
        for x in range(contraption.width):
            yield Vector(x, 0), Direction.Down
        for y in range(contraption.height):
            yield Vector(contraption.width - 1, y), Direction.Left
        for x in range(contraption.width - 1, -1, -1):
            yield Vector(x, contraption.height - 1), Direction.Up
        for y in range(contraption.height - 1, -1, -1):
            yield Vector(0, y), Direction.Right

    def solve_part1(self, input_str: str) -> str:
        contraption = self.parse_input(input_str)
        beams = [LightBeam(location=Vector(0, 0), direction=Direction.Right)]
        self.simulate(contraption=contraption, beams=beams)
        return str(contraption.calc_energised_tiles_and_reset())

    def solve_part2(self, input_str: str) -> str:
        contraption = self.parse_input(input_str)
        result = 0
        for v, d in self.iter_edge_with_dirs(contraption):
            self.simulate(contraption, [LightBeam(v, d)])
            et = contraption.calc_energised_tiles_and_reset()
            if et > result:
                result = et
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=16, part=1, s_class=Day16, path_prefix='..')
    run_puzzle(day=16, part=2, s_class=Day16, path_prefix='..')
