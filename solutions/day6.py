import bisect
import math
from typing import NamedTuple, Callable

from common import Day, line_iterator


class RaceResult(NamedTuple):
    race: 'Race'
    button_time: int
    distance: int

    @property
    def won(self):
        return self.distance > self.race.best_distance


class Race(NamedTuple):
    time: int
    best_distance: int

    def simulate_race(self, button_time: int) -> RaceResult:
        if not 0 <= button_time <= self.time:
            raise ValueError(f'invalid hold time ({button_time} ms), for this race ({self})')
        return RaceResult(self, button_time, (self.time - button_time) * button_time)


class Day6(Day):
    @staticmethod
    def parse_input(input_str: str, process_line: Callable[[str], str]) -> list[Race]:
        times = None
        distances = None
        races = []
        for line in line_iterator(input_str):
            if line.startswith('Time:'):
                times = [int(n) for n in process_line(line[5:]).split(' ') if n]
            elif line.startswith('Distance:'):
                distances = [int(n) for n in process_line(line[9:]).split(' ') if n]
        for time, distance in zip(times, distances):
            races.append(Race(time=time, best_distance=distance))
        return races

    @staticmethod
    def do_the_math(races: list[Race]) -> int:
        result = 0
        for race in races:
            r = range(0, math.floor(race.time / 2) + 1, 1)
            win_start = bisect.bisect_right(a=r, x=race.best_distance, key=lambda bt: race.simulate_race(bt).distance)
            win_count = (r.stop - win_start) * 2
            if race.time % 2 == 0:
                win_count -= 1
            result = win_count if result == 0 else result * win_count
        return result

    def solve_part1(self, input_str: str) -> str:
        races = self.parse_input(input_str=input_str, process_line=str.strip)
        result = self.do_the_math(races)
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        races = self.parse_input(input_str=input_str, process_line=lambda s: s.replace(' ', ''))
        result = self.do_the_math(races)
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=6, part=1, s_class=Day6, path_prefix='..')
    run_puzzle(day=6, part=2, s_class=Day6, path_prefix='..')
