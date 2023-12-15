import re

from common import Day


step_regex = re.compile(r'^(\w+)([-=])(\d)?')


class Day15(Day):
    @staticmethod
    def hash_string(s: str) -> int:
        result = 0
        for c in s:
            result = ((result + ord(c)) * 17) % 256
        return result

    def solve_part1(self, input_str: str) -> str:
        steps = input_str.split(',')
        result = 0
        for step in steps:
            result += self.hash_string(step)
        return str(result)

    def solve_part2(self, input_str: str) -> str:
        steps = input_str.split(',')
        boxes: list[list[tuple[str, int]]] = [[] for _ in range(256)]
        for step in steps:
            match = step_regex.fullmatch(step)
            label, operator, focal_len = match[1], match[2], match[3]
            box = boxes[self.hash_string(label)]
            lens_index = next((i for i, lens in enumerate(box) if lens[0] == label), None)
            if operator == '-':
                if lens_index is not None:
                    box.pop(lens_index)
            elif operator == '=':
                new_lens = (label, int(focal_len))
                if lens_index is None:
                    box.append(new_lens)
                else:
                    box[lens_index] = new_lens
        result = 0
        for box_id, box in enumerate(boxes):
            for lens_index, lens in enumerate(box):
                result += (box_id + 1) * (lens_index + 1) * lens[1]
        return str(result)


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=15, part=1, s_class=Day15, path_prefix='..')
    run_puzzle(day=15, part=2, s_class=Day15, path_prefix='..')
