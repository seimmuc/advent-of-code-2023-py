from functools import cached_property
from itertools import pairwise
from typing import Iterator

from common import Day, line_iterator


class Day9Sequence:
    def __init__(self, numbers: list[int]):
        self.numbers = numbers

    @cached_property
    def is_zeroes(self) -> bool:
        return all(n == 0 for n in self.numbers)

    @cached_property
    def increment_sequence(self) -> 'Day9Sequence':
        return Day9Sequence(numbers=[n2 - n1 for n1, n2 in pairwise(self.numbers)])

    def predict_next_num(self) -> int:
        if self.is_zeroes:
            return 0
        next_increment = self.increment_sequence.predict_next_num()
        return self.numbers[-1] + next_increment

    def predict_prev_num(self) -> int:
        if self.is_zeroes:
            return 0
        prev_increment = self.increment_sequence.predict_prev_num()
        return self.numbers[0] - prev_increment


class Day9(Day):
    @staticmethod
    def iter_input(input_str: str) -> Iterator[Day9Sequence]:
        for line in line_iterator(input_str):
            yield Day9Sequence(numbers=[int(n.strip()) for n in line.split(' ') if n])

    def solve_part1(self, input_str: str) -> str:
        return str(sum(seq.predict_next_num() for seq in self.iter_input(input_str)))

    def solve_part2(self, input_str: str) -> str:
        return str(sum(seq.predict_prev_num() for seq in self.iter_input(input_str)))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=9, part=1, s_class=Day9, path_prefix='..')
    run_puzzle(day=9, part=2, s_class=Day9, path_prefix='..')
