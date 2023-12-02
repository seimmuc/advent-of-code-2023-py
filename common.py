from abc import ABC, abstractmethod
from io import StringIO
from typing import Iterator


class Day(ABC):
    @abstractmethod
    def solve_part1(self, input_str: str) -> str:
        raise NotImplemented

    @abstractmethod
    def solve_part2(self, input_str: str) -> str:
        raise NotImplemented


def line_iterator(multiline_string: str, strip_newline: bool = True) -> Iterator[str]:
    for line in StringIO(multiline_string):
        if strip_newline:
            line = line.rstrip('\r\n')
        yield line
