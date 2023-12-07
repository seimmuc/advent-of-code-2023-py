from enum import IntEnum
from functools import cached_property, total_ordering
from itertools import chain
from typing import Iterable, Type

from common import Day, line_iterator


CARDS = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_STRENGTHS_PART1 = {c: len(CARDS) - i for i, c in enumerate(CARDS)}
CARD_STRENGTHS_PART2 = {c: len(CARDS) - i for i, c in chain(enumerate(c for c in CARDS if c != 'J'),
                                                            [(len(CARDS) - 1, 'J')])}


class CamelCardsHandType(IntEnum):
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0


@total_ordering
class CamelCardsHand:
    CARD_STRENGTHS = CARD_STRENGTHS_PART1

    def __init__(self, cards: str | Iterable[str]):
        if not isinstance(cards, str):
            cards = ''.join(cards)
        if len(cards) != 5:
            raise ValueError('hand must have 5 cards!')
        self.cards = cards

    def as_dict(self) -> dict[str, int]:
        d: dict[str, int] = {}
        for c in self.cards:
            d[c] = d[c] + 1 if c in d else 1
        return d

    @staticmethod
    def type_from_distribution_list(d_list: list[int]):
        m = max(d_list)
        if m == 5:
            return CamelCardsHandType.FIVE_OF_A_KIND
        if m == 4:
            return CamelCardsHandType.FOUR_OF_A_KIND
        if m == 3:
            if 2 in d_list:
                return CamelCardsHandType.FULL_HOUSE
            else:
                return CamelCardsHandType.THREE_OF_A_KIND
        if 2 in d_list:
            if sum(1 if n == 2 else 0 for n in d_list) == 2:
                return CamelCardsHandType.TWO_PAIR
            else:
                return CamelCardsHandType.ONE_PAIR
        return CamelCardsHandType.HIGH_CARD

    def _calc_type(self) -> CamelCardsHandType:
        return self.type_from_distribution_list(list(self.as_dict().values()))

    @cached_property
    def type(self) -> CamelCardsHandType:
        return self._calc_type()

    def __eq__(self, other: 'CamelCardsHand') -> bool:
        return self.cards == other.cards

    def __lt__(self, other: 'CamelCardsHand') -> bool:
        if self.type != other.type:
            return self.type < other.type
        for i in range(5):
            if self.cards[i] == other.cards[i]:
                continue
            return self.CARD_STRENGTHS[self.cards[i]] < self.CARD_STRENGTHS[other.cards[i]]
        return False


class CamelCardsHandPart2(CamelCardsHand):
    CARD_STRENGTHS = CARD_STRENGTHS_PART2

    def _calc_type(self) -> CamelCardsHandType:
        d = self.as_dict()          # split cards by type
        j = d.pop('J', 0)           # move jokers aside
        if not d:                   # special case: if all cards were jokers, it's a FIVE_OF_A_KIND
            return CamelCardsHandType.FIVE_OF_A_KIND
        dv = list(d.values())
        m = max(dv)                 # find most highest same-type card count
        dv[dv.index(m)] = m + j     # "replace" jokers with that card type
        return self.type_from_distribution_list(dv)


class Day7(Day):
    @staticmethod
    def parse_input(input_str: str, hand_class: Type[CamelCardsHand]) -> list[tuple[CamelCardsHand, int]]:
        hands_and_bids = []
        hand_strs = set()
        for line in line_iterator(input_str):
            line = line.split(' ')
            hands_and_bids.append((hand_class(line[0]), int(line[1])))
            if line[0] in hand_strs:
                raise RuntimeError()
            hand_strs.add(line[0])
        return hands_and_bids

    @staticmethod
    def calc_total_winnings(hands_and_bids: list[tuple[CamelCardsHand, int]]) -> int:
        hands_and_bids.sort(key=lambda e: e[0])  # sort in-place based on hand
        result = 0
        for i, (hand, bid) in enumerate(hands_and_bids):
            # why are you like this pycharm? whyyyyy?
            # noinspection PyTypeChecker
            result += bid * (i + 1)  # bid * rank
        return result

    def solve_part1(self, input_str: str) -> str:
        hands_and_bids = self.parse_input(input_str, hand_class=CamelCardsHand)
        return str(self.calc_total_winnings(hands_and_bids))

    def solve_part2(self, input_str: str) -> str:
        hands_and_bids = self.parse_input(input_str, hand_class=CamelCardsHandPart2)
        return str(self.calc_total_winnings(hands_and_bids))


if __name__ == '__main__':
    from main import run_puzzle
    run_puzzle(day=7, part=1, s_class=Day7, path_prefix='..')
    run_puzzle(day=7, part=2, s_class=Day7, path_prefix='..')
