from bisect import bisect_left
from functools import cache
from typing import Iterator, Callable

from common import Day, line_iterator


class SpringRecordRow:
    def __init__(self, line: str, damaged_criteria: list[int]):
        self.ln = tuple(line)
        self.damaged_criteria = damaged_criteria
        self.valid_placements: dict[int, list[int]] = {cgs: list(self.iter_cg_placements_all(cgs, 0))
                                                       for cgs in set(damaged_criteria)}

    # Unused methods
    # @property
    # def iter_arrangements(self) -> Iterator[list[str]]:
    #     l = list(self.ln)
    #     unknown_indexes = list(i for i, x in enumerate(l) if x == '?')
    #     damaged_spring_count = sum(1 for s in l if s == '#')
    #     for c in combinations(iterable=unknown_indexes, r=sum(self.damaged_criteria) - damaged_spring_count):
    #         for i in unknown_indexes:
    #             l[i] = '.'
    #         for i in c:
    #             l[i] = '#'
    #         yield l
    #
    # def matches_damaged_criteria(self, l: list[str]) -> bool:
    #     dcl = reduce(self.__dmgr, l, [0])
    #     if dcl[-1] == 0:
    #         dcl.pop(-1)
    #     return dcl == self.damaged_criteria
    #
    # @staticmethod
    # def __dmgr(l: list[int], s: str) -> list[int]:
    #     if s == '#':
    #         l[-1] += 1
    #     elif l[-1] != 0:
    #         l.append(0)
    #     return l

    def iter_cg_placements_all(self, cg_size: int, start_index: int) -> Iterator[int]:
        ln = self.ln
        for i in range(start_index, len(ln) - cg_size + 1):
            # if prev char and one after `cg_size` other chars can be '.' and everything in between can be '#'
            if (i == 0 or ln[i - 1] != '#') and (i + cg_size == len(ln) or ln[i + cg_size] != '#') \
                    and all(ln[j] == '#' or ln[j] == '?' for j in range(i, i + cg_size)):
                yield i

    @cache
    def iter_cg_placements(self, cg_size: int, start_index: int) -> list[int]:
        r = []
        oi = start_index
        vp = self.valid_placements[cg_size]
        for i in range(bisect_left(vp, start_index), len(vp)):
            if self.contains_damaged(oi, vp[i]):
                return r
            r.append(vp[i])
            oi = vp[i]
        return r

    @cache
    def contains_damaged(self, start: int, end: int) -> bool:
        return any(self.ln[i] == '#' for i in range(start, end))


class Day12(Day):
    @staticmethod
    def iter_input(input_str: str, unfold_func: Callable[[str, str], tuple[str, str]]) -> Iterator[SpringRecordRow]:
        for line in line_iterator(input_str):
            rl, dc = line.split(' ', maxsplit=1)    # type: str, str
            rl, dc = unfold_func(rl, dc)
            yield SpringRecordRow(line=rl, damaged_criteria=[int(n.strip()) for n in dc.split(',')])

    @classmethod
    @cache
    def count_arrangements(cls, record: SpringRecordRow, cg_num: int = 0, start_at: int = 0) -> int:
        cgp_iter = record.iter_cg_placements(record.damaged_criteria[cg_num], start_at)
        if cg_num + 1 >= len(record.damaged_criteria):  # if we're at the last contiguous group criteria
            return sum(1 for cgp in cgp_iter
                       if not record.contains_damaged(cgp + record.damaged_criteria[cg_num] + 1, len(record.ln)))
        result = 0
        for cgp in cgp_iter:
            result += cls.count_arrangements(record, cg_num + 1, cgp + record.damaged_criteria[cg_num] + 1)
        return result

    def solve_part1(self, input_str: str) -> str:
        result = 0
        for record in self.iter_input(input_str, lambda x, y: (x, y)):
            arr = self.count_arrangements(record=record)
            result += arr
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        result = 0
        for record in self.iter_input(input_str, lambda x, y: ('?'.join([x] * 5), ','.join([y] * 5))):
            arr = self.count_arrangements(record=record)
            result += arr
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=12, part=1, s_class=Day12, path_prefix='..')
    run_puzzle(day=12, part=2, s_class=Day12, path_prefix='..')
