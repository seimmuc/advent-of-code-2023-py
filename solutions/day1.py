from typing import Iterable

from common import Day, line_iterator


DIGIT_NAMES = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


class Day1(Day):
    DIGITS = [str(i) for i in range(0, 10)]
    DIGITS_WITH_NAMES = {str(i): i for i in range(0, 10)}
    DIGITS_WITH_NAMES.update({n: i for i, n in enumerate(DIGIT_NAMES)})

    def solve_part1(self, input_str: str) -> str:
        result = 0
        for line in line_iterator(input_str):
            line_digits = [c for c in line if c in self.DIGITS]
            result += int(line_digits[0] + line_digits[-1])
        return str(result)

    @classmethod
    def find_a_digit(cls, line: str, index_iter: Iterable[int], max_len: int) -> int | None:
        for i in index_iter:
            substr = line[i:i+max_len]
            for dn in cls.DIGITS_WITH_NAMES:
                if substr.startswith(dn):
                    return cls.DIGITS_WITH_NAMES[dn]
        return None

    def solve_part2(self, input_str: str) -> str:
        max_len = max((len(s) for s in self.DIGITS_WITH_NAMES.keys()))
        result = 0
        for line in line_iterator(input_str):
            first_digit = self.find_a_digit(line, range(0, len(line), 1), max_len)
            last_digit = self.find_a_digit(line, range(len(line) - 1, -1, -1), max_len)
            result += int(str(first_digit) + str(last_digit))
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=1, part=1, s_class=Day1)
    run_puzzle(day=1, part=2, s_class=Day1)
