import itertools
import math
import re
from functools import cached_property
from typing import Tuple, Literal, Iterable, Callable

from common import Day, line_iterator


node_regex = re.compile(r'(\w{3}) = \((\w{3}), (\w{3})\)')


class Day8Node:
    def __init__(self, name: str, left_node_name: str, right_node_name: str, all_nodes: dict[str, 'Day8Node']):
        self.name = name
        self.all_nodes = all_nodes
        self.left_node_name = left_node_name
        self.right_node_name = right_node_name

    @cached_property
    def left_node(self) -> 'Day8Node':
        return self.all_nodes[self.left_node_name]

    @cached_property
    def right_node(self) -> 'Day8Node':
        return self.all_nodes[self.right_node_name]

    def get_node_at(self, direction: Literal['R', 'L']) -> 'Day8Node':
        if direction == 'L':
            return self.left_node
        if direction == 'R':
            return self.right_node
        raise RuntimeError('invalid direction')


class Day8Travel:
    def __init__(self, start_node: Day8Node, directions: Iterable[Literal['R', 'L']], all_nodes: dict[str, 'Day8Node'],
                 end_condition: Callable[[str], bool]):
        self.start_node = start_node
        self.directions = directions
        self.all_nodes = all_nodes
        self.end_condition = end_condition

    @cached_property
    def travel_length(self) -> int:
        length = 0
        ec = self.end_condition
        current_node = self.start_node
        for direction in itertools.cycle(self.directions):
            current_node = current_node.get_node_at(direction)
            length += 1
            if ec(current_node.name):
                break
        return length


class Day8(Day):
    @staticmethod
    def parse_input(input_str: str) -> Tuple[Iterable[Literal['R', 'L']], dict[str, Day8Node]]:
        li = line_iterator(input_str)
        turns: str = next(li).strip()
        if len(turns.replace('R', '').replace('L', '')) > 0:
            raise RuntimeError('turns contains invalid characters')
        nodes: dict[str, Day8Node] = {}
        next(li)
        for line in li:
            match = node_regex.fullmatch(line.strip())
            node = Day8Node(name=match[1], left_node_name=match[2], right_node_name=match[3], all_nodes=nodes)
            nodes[node.name] = node
        # noinspection PyTypeChecker
        return turns, nodes

    def solve_part1(self, input_str: str) -> str:
        turns, nodes = self.parse_input(input_str)
        travel = Day8Travel(start_node=nodes['AAA'], directions=turns, all_nodes=nodes,
                            end_condition=lambda n: n == 'ZZZ')
        return str(travel.travel_length)

    def solve_part2(self, input_str: str) -> str:
        turns, nodes = self.parse_input(input_str)
        all_travels = [Day8Travel(start_node=node, directions=turns, all_nodes=nodes,
                                  end_condition=lambda n: n.endswith('Z'))
                       for node in nodes.values() if node.name.endswith('A')]
        distances = list(tr.travel_length for tr in all_travels)
        return str(math.lcm(*distances))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=8, part=1, s_class=Day8, path_prefix='..')
    run_puzzle(day=8, part=2, s_class=Day8, path_prefix='..')
