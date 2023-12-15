from common import Day, Grid, Vector, line_iterator, Direction


class RockPlatform(Grid[str]):
    def calc_load_north(self) -> int:
        load, h = 0, self.height
        for p, v in self.scan_all():
            if v == 'O':
                load += h - p.y
        return load

    def scan_in_cardinal_dir(self, d: Direction):
        if d.value[1] != 0:
            for y in range(self.height) if d.value[1] > 0 else range(self.height - 1, -1, -1):
                for x in range(self.width):
                    v = Vector(x, y)
                    yield v, self.get_cell(v)
        else:
            for x in range(self.width) if d.value[0] > 0 else range(self.width - 1, -1, -1):
                for y in range(self.height):
                    v = Vector(x, y)
                    yield v, self.get_cell(v)


class Day14(Day):
    @staticmethod
    def parse_input(input_str: str) -> RockPlatform:
        platform = RockPlatform()
        for line in line_iterator(input_str):
            platform.add_line(list(line))
        return platform

    @staticmethod
    def roll_rock(platform: RockPlatform, start_vec: Vector, direction: Direction):
        rock = platform.get_cell(start_vec)
        end_vec, c_vec = start_vec, start_vec.move_in(direction)
        while platform.is_in_bounds(c_vec) and platform.get_cell(c_vec) == '.':
            end_vec = c_vec
            c_vec = c_vec.move_in(direction)
        if end_vec != start_vec:
            platform.set_cell(end_vec, rock)
            platform.set_cell(start_vec, '.')

    def solve_part1(self, input_str: str) -> str:
        platform = self.parse_input(input_str)
        for pos, val in platform.scan_in_cardinal_dir(Direction.Down):
            if val == 'O':
                self.roll_rock(platform=platform, start_vec=pos, direction=Direction.Up)
        for ln in platform.lines:
            print(''.join(ln))
        return str(platform.calc_load_north())

    def solve_part2(self, input_str: str) -> str:
        platform = self.parse_input(input_str)
        spin_dirs = [Direction.Up, Direction.Left, Direction.Down, Direction.Right]
        repetitions_needed = 1
        target_cycle = 1000000000
        cycle_results = []
        for i in range(target_cycle):
            for d in spin_dirs:
                for p, v in platform.scan_in_cardinal_dir(d.inverse):
                    if v == 'O':
                        self.roll_rock(platform, p, d)
            cycle_results.append(platform.calc_load_north())
            for rep_len in range(1, len(cycle_results) // repetitions_needed):
                ref = cycle_results[-rep_len:]
                if all(cycle_results[j: j + rep_len] == ref
                       for j in range(len(cycle_results) - rep_len * 2,
                                      len(cycle_results) - rep_len * (repetitions_needed + 2), -rep_len)):
                    cycles_left = target_cycle - 1 - i
                    return str(ref[(cycles_left - 1) % rep_len])
        return str(cycle_results[-1])


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=14, part=1, s_class=Day14, path_prefix='..')
    run_puzzle(day=14, part=2, s_class=Day14, path_prefix='..')
