import re
from typing import NamedTuple, Iterator

from common import Day, line_iterator, batch_iterator


seeds_regex = re.compile(r'seeds:((:? \d+)+)')
group_regex = re.compile(r'([\w]+)-to-([\w]+) map:\n((?:\d+[ |\n]?)+)')


class AlmanacMapConversion:
    def __init__(self, destination_start: int, source_start: int, map_range: int):
        self.source_range = range(source_start, source_start + map_range, 1)
        self.destination_range = range(destination_start, destination_start + map_range, 1)


class AlmanacMap(NamedTuple):
    source: str
    destination: str
    conversions: list[AlmanacMapConversion]

    def convert(self, source_num: int):
        for c in self.conversions:
            if source_num in c.source_range:
                return c.destination_range[source_num - c.source_range.start]
        return source_num

    def current_range_over_in(self, source_num: int) -> int | None:
        nr_start: int | None = None
        for c in self.conversions:
            if source_num in c.source_range:
                return c.source_range.stop - source_num
            if c.source_range.start > source_num and (nr_start is None or c.source_range.start < nr_start):
                nr_start = c.source_range.start
        return None if nr_start is None else nr_start - source_num


class Almanac:
    def __init__(self):
        self.seeds_numbers: list[int] = []
        self.conversion_maps: dict[str, AlmanacMap] = {}

    def map_chain(self, source_category: str, destination_category: str) -> Iterator[AlmanacMap]:
        category = source_category
        while category != destination_category:
            cmap = next((cm for cm in self.conversion_maps.values() if cm.source == category), None)
            if cmap is None:
                return RuntimeError(f'{category} cannot be converted into anything else')
            yield cmap
            category = cmap.destination

    def convert_to(self, number: int, source_category: str, destination_category: str):
        for cmap in self.map_chain(source_category, destination_category):
            number = cmap.convert(number)
        return number


class Day5(Day):
    @staticmethod
    def parse_input(input_str: str) -> Almanac:
        almanac = Almanac()
        match = seeds_regex.search(input_str)
        almanac.seeds_numbers = [int(n) for n in match[1].split(' ') if n]
        for match in group_regex.finditer(input_str):
            a_map = AlmanacMap(source=match[1], destination=match[2], conversions=[])
            for line in line_iterator(match[3]):
                line_nums = [int(n) for n in line.split(' ') if n]
                a_map.conversions.append(AlmanacMapConversion(line_nums[0], line_nums[1], line_nums[2]))
            almanac.conversion_maps[f'{a_map.source}-{a_map.destination}'] = a_map
        return almanac

    def solve_part1(self, input_str: str) -> str:
        almanac = self.parse_input(input_str)
        result = None
        for seed in almanac.seeds_numbers:
            num = almanac.convert_to(number=seed, source_category='seed', destination_category='location')
            if result is None or num < result:
                result = num
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        almanac = self.parse_input(input_str)
        result = None

        seed_ranges: list[range] = [range(s, s + l) for s, l in batch_iterator(almanac.seeds_numbers, 2, False)]

        # Useless optimisation 1: it roughly cuts full conversion (seed > location) time in half
        conversions = list(almanac.map_chain(source_category='seed', destination_category='location'))

        # Useless optimisation 2: turns out ranges don't actually overlap (at least in my case) and it wouldn't really
        # do much even if they did. I don't know why thought it'd be a good idea to waste time doing this.
        seed_ranges.sort(key=lambda r: r.start)
        seed_ranges_no_overlap: list[range] = seed_ranges[0:1]
        for sr in seed_ranges[1:]:
            lsr = seed_ranges_no_overlap[-1]
            if lsr.stop >= sr.start:
                seed_ranges_no_overlap[-1] = range(lsr.start, max(lsr.stop, sr.stop))
            else:
                seed_ranges_no_overlap.append(sr)

        for r in seed_ranges_no_overlap:
            i = r.start
            while i < r.stop:
                incr: int | None = None
                num: int = i
                for c in conversions:
                    # Figure out how long the conversion difference will remain unchanged if we kept incrementing source
                    # This optimisation cuts down number of required checks from 1753244662 down to 82 (with my input)
                    rl = c.current_range_over_in(num)
                    if rl is not None and (incr is None or rl < incr):
                        incr = rl
                    num = c.convert(num)
                if result is None or num < result:
                    result = num
                if incr is None:
                    break
                i += incr
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=5, part=1, s_class=Day5, path_prefix='..')
    run_puzzle(day=5, part=2, s_class=Day5, path_prefix='..')
