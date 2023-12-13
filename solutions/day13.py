from typing import Iterator

from common import Day, Grid, line_iterator


class Day13(Day):
    @classmethod
    def find_all_reflections(cls, seq_iter: Iterator[list[str]], smudge_count: int) -> list[int] | None:
        options: dict[int, int] | None = None
        for seq in seq_iter:
            if options is None:
                options = {i: smudge_count for i in range(1, len(seq))}
            # noinspection PyTypeChecker
            ou = list(cls.check_reflection_options(seq, options.items()))
            for i, sl in ou:
                if sl < 0:
                    del options[i]
                else:
                    options[i] = sl
            if not options:
                break
        return list(i for i, sl in options.items() if sl == 0)

    @staticmethod
    def check_reflection_options(seq: list[str], options: Iterator[tuple[int, int]]) -> Iterator[tuple[int, int]]:
        for i, err_left in options:
            size = min(i, len(seq) - i)
            for j in range(size):
                if seq[i + j] != seq[i - j - 1]:
                    err_left -= 1
                    if err_left < 0:
                        break
            yield i, err_left

    @staticmethod
    def iter_input(input_str: str) -> Iterator[Grid[str]]:
        c_pattern: Grid[str] = Grid()
        for line in line_iterator(input_str):
            if line:
                c_pattern.add_line(line=line)
                continue
            if c_pattern.height > 0:
                yield c_pattern
                c_pattern = Grid()
        if c_pattern.height > 0:
            yield c_pattern

    @classmethod
    def do_math(cls, pat_iter: Iterator[Grid[str]], smudge_count: int = 0) -> int:
        result, sm = 0, smudge_count
        for pat in pat_iter:
            m = 1
            refl = cls.find_all_reflections((list(s for _, s in pat.scan_row(y)) for y in range(pat.height)), sm)
            if not refl:
                refl = cls.find_all_reflections((list(s for _, s in pat.scan_column(x)) for x in range(pat.width)), sm)
                m = 100
            if len(refl) != 1:
                raise RuntimeError()
            result += refl.pop() * m
        return result

    def solve_part1(self, input_str: str) -> str:
        return str(self.do_math(pat_iter=self.iter_input(input_str)))

    def solve_part2(self, input_str: str) -> str:
        return str(self.do_math(pat_iter=self.iter_input(input_str), smudge_count=1))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=13, part=1, s_class=Day13, path_prefix='..')
    run_puzzle(day=13, part=2, s_class=Day13, path_prefix='..')
