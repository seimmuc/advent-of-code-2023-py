import re
from typing import NamedTuple

from common import Day, line_iterator


regex_game_line = re.compile(r'Game (\d+): (.*)')
regex_draw = re.compile(r'(\d+) (\w+)')


class Day2GameDraw(NamedTuple):
    red: int
    green: int
    blue: int


class Day2GameRound(NamedTuple):
    game_id: int
    draws: list[Day2GameDraw]


class Day2(Day):
    @staticmethod
    def parse_line(line: str) -> Day2GameRound:
        match = regex_game_line.fullmatch(line)
        g_round = Day2GameRound(int(match[1]), [])
        draw_strs = match[2].split(';')
        for draw_str in draw_strs:
            colors = {}
            for c_str in draw_str.split(','):
                match = regex_draw.fullmatch(c_str.strip())
                colors[match[2]] = int(match[1])
            g_round.draws.append(Day2GameDraw(red=colors.get('red', 0), green=colors.get('green', 0),
                                              blue=colors.get('blue', 0)))
        return g_round

    def solve_part1(self, input_str: str) -> str:
        max_red = 12
        max_green = 13
        max_blue = 14
        result = 0
        for line in line_iterator(input_str):
            game = self.parse_line(line)
            possible = True
            for draw in game.draws:
                if draw.red > max_red or draw.green > max_green or draw.blue > max_blue:
                    possible = False
                    break
            if possible:
                result += game.game_id
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        result = 0
        for line in line_iterator(input_str):
            game = self.parse_line(line)
            min_cubes = [max(d[col] for d in game.draws) for col in range(3)]
            result += min_cubes[0] * min_cubes[1] * min_cubes[2]
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=2, part=1, s_class=Day2, path_prefix='..')
    run_puzzle(day=2, part=2, s_class=Day2, path_prefix='..')
