from importlib import import_module
from pathlib import Path
from types import ModuleType, NoneType
from typing import Literal, Dict, Type

from common import Day


dir_names = {'inputs': 'inputs', 'solutions': 'solutions'}


def run_puzzle(day: int, part: Literal[1, 2], version: str = None, s_module: str | ModuleType = None,
               s_class: str | Type[Day] = None, s_inst_kwargs: Dict = None, s_instance: Day = None,
               input_file: str = None):
    if part not in (1, 2):
        raise ValueError(f'Invalid part: {part}')
    if s_instance is None:
        if isinstance(s_class, (str, NoneType)):
            if not isinstance(s_module, ModuleType):
                if s_module is None:
                    s_module = f'day{day}'
                s_module = import_module(f'{dir_names["solutions"]}.{s_module}')
            if s_class is None:
                s_class = f'Day{day}'
                if version:
                    s_class += f'V_{version}'
            s_class = getattr(s_module, s_class)
        day_class: Type[Day] = s_class
        # noinspection PyArgumentList
        s_instance = day_class(**({} if s_inst_kwargs is None else s_inst_kwargs))
    solve_method = s_instance.solve_part1 if part == 1 else s_instance.solve_part2

    if input_file is None:
        input_file = f'd{day}.txt'
    else:
        print(f'using alternative input file "{input_file}"')
    with Path(dir_names['inputs'], input_file).open(mode='rt', encoding='utf8', newline='\n') as f:
        puzzle_input = f.read()
    print(f'Solving day {day} part {part}', '' if version is None else f' ({version})', sep='')
    # noinspection PyArgumentList
    solution_output = solve_method(input_str=puzzle_input)
    if isinstance(solution_output, str):
        print('Done, printing solution')
        print('=======================')
        print(solution_output)
        print('=======================')
    else:
        print(f'Error: solution output is of invalid type: {type(solution_output)}')


if __name__ == '__main__':
    example_input = True
    in_file = 'example_input.txt' if example_input else None
    run_puzzle(day=1, part=1, input_file=in_file)
