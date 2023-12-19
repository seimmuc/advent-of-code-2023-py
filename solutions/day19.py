import operator
import re
from functools import reduce
from typing import NamedTuple, Literal

from common import Day, line_iterator


workflow_regex = re.compile(r'(\w+){(.+)}')
conditional_rule_regex = re.compile(r'(\w)([<>])(\d+):(\w+)')
simple_rule_regex = re.compile(r'\w+')
part_regex = re.compile(r'{(?:\w=\d+,?){4}}')
OPERATORS = {'<': operator.lt, '>': operator.gt}


class Day19Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


class Day19PartHypothetical(NamedTuple):
    x: range = range(1, 4001)
    m: range = range(1, 4001)
    a: range = range(1, 4001)
    s: range = range(1, 4001)

    @property
    def total_size(self) -> int:
        return reduce(lambda x, y: x * y, (len(r) for r in self))

    def replace_range(self, cat: str, new_range: range):
        return Day19PartHypothetical(*(new_range if c == cat else r for r, c in zip(self, ('x', 'm', 'a', 's'))))

    def split_on(self, cat: str, opr: Literal['<', '>'], val: int)\
            -> tuple['Day19PartHypothetical | None', 'Day19PartHypothetical | None']:
        current_range: range = getattr(self, cat)
        if opr == '<':
            r1 = range(current_range.start, min(current_range.stop, val))
            r2 = range(max(current_range.start, val), current_range.stop)
        else:
            r1 = range(max(current_range.start, val + 1), current_range.stop)
            r2 = range(current_range.start, min(current_range.stop, val + 1))
        p1 = None if len(r1) < 1 else self.replace_range(cat, r1)
        p2 = None if len(r2) < 1 else self.replace_range(cat, r2)
        return p1, p2


class Day19Rule:
    def __init__(self, cat: str, opr: Literal['<', '>'] | None, val: int, destination: str):
        self.cat = cat
        self.opr = opr
        self.val = val
        self.destination = destination

    def matches(self, part: Day19Part):
        return self.opr is None or OPERATORS[self.opr](getattr(part, self.cat), self.val)

    def __repr__(self):
        if self.opr is None:
            return f'SimpleRule({self.destination})'
        return f'Rule({self.cat}, {self.opr.__name__}, {self.val}, {self.destination})'

    @staticmethod
    def from_str(s: str) -> 'Day19Rule':
        if simple_rule_regex.fullmatch(s):
            return Day19Rule('', None, 0, s.strip())
        match = conditional_rule_regex.fullmatch(s)
        return Day19Rule(match[1], match[2], int(match[3]), match[4])


class Day19Workflow:
    def __init__(self, name: str, rules: list[Day19Rule]):
        if any(r.opr is None for r in rules[:-1]) or rules[-1].opr is not None:
            raise RuntimeError(f'Invalid workflow rules: {rules}')
        self.name = name
        self.rules = rules

    def process_part(self, part: Day19Part) -> str:
        for rule in self.rules:
            if rule.matches(part):
                return rule.destination
        raise RuntimeError('something is wrong')

    def __repr__(self):
        return f'Workflow({self.name}, {self.rules})'

    @staticmethod
    def from_line(input_line: str) -> 'Day19Workflow':
        match = workflow_regex.fullmatch(input_line)
        workflow = Day19Workflow(match[1], [Day19Rule.from_str(s) for s in match[2].split(',')])
        return workflow


class Day19(Day):
    @staticmethod
    def parse_input(input_str: str) -> tuple[dict[str, Day19Workflow], list[Day19Part]]:
        workflows: dict[str, Day19Workflow] = {}
        parts: list[Day19Part] = []
        line_iter = line_iterator(input_str)
        for line in line_iter:
            if not line:
                break
            wf = Day19Workflow.from_line(line)
            workflows[wf.name] = wf
        for line in line_iter:
            if not part_regex.fullmatch(line):
                raise RuntimeError(f'Part "{line}" has invalid syntax')
            parts.append(Day19Part(**{rs[0]: int(rs[2:]) for rs in line[1:-1].split(',')}))
        return workflows, parts

    def solve_part1(self, input_str: str) -> str:
        workflows, parts = self.parse_input(input_str)
        first_workflow = workflows['in']
        result = 0
        for part in parts:
            wf = first_workflow
            while True:
                des = wf.process_part(part)
                if des == 'A':
                    result += sum(part)
                    break
                if des == 'R':
                    break
                wf = workflows[des]
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        workflows, _ = self.parse_input(input_str)
        parts: list[tuple[Day19PartHypothetical, str]] = [(Day19PartHypothetical(), 'in')]
        result = 0
        while parts:
            part, wf_name = parts.pop()
            if wf_name in ('A', 'R'):
                if wf_name == 'A':
                    result += part.total_size
                continue
            workflow = workflows[wf_name]
            for rule in workflow.rules:
                if rule.opr is None:
                    parts.append((part, rule.destination))
                else:
                    # noinspection PyTypeChecker
                    m_part, nm_part = part.split_on(rule.cat, rule.opr, rule.val)
                    if m_part is not None:
                        parts.append((m_part, rule.destination))
                    if nm_part is None:
                        break
                    part = nm_part
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=19, part=1, s_class=Day19, path_prefix='..')
    run_puzzle(day=19, part=2, s_class=Day19, path_prefix='..')
