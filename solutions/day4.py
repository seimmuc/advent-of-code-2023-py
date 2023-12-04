import re

from common import Day, line_iterator


line_regex = re.compile(r'Card +(\d+): ([\d ]+) \| ([\d ]+)')


class Day4Line:
    def __init__(self, card_id: int, winning_nums: list[int], your_nums: list[int]):
        self.card_id = card_id
        self.winning_nums = winning_nums
        self.your_nums = your_nums
        self.copy_count = 1


class Day4(Day):
    @staticmethod
    def parse_line(line: str) -> Day4Line:
        match = line_regex.fullmatch(line)
        cid = int(match[1])
        w_nums = [int(n) for n in match[2].split(' ') if n]
        y_nums = [int(n) for n in match[3].split(' ') if n]
        return Day4Line(cid, w_nums, y_nums)

    def solve_part1(self, input_str: str) -> str:
        result = 0
        for line in line_iterator(input_str):
            d4l = self.parse_line(line)
            points = 0
            for n in d4l.your_nums:
                if n in d4l.winning_nums:
                    points = 1 if points == 0 else points * 2
            result += points
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        d4lines = [self.parse_line(line) for line in line_iterator(input_str)]
        for ci, d4l in enumerate(d4lines):
            matches = sum(1 for n in d4l.your_nums if n in d4l.winning_nums)
            for i in range(ci + 1, min(len(d4lines), ci + 1 + matches), 1):
                d4lines[i].copy_count += d4l.copy_count
        return str(sum(d4l.copy_count for d4l in d4lines))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=4, part=1, s_class=Day4, path_prefix='..')
    run_puzzle(day=4, part=2, s_class=Day4, path_prefix='..')
