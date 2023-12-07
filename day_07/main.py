import functools
from collections import defaultdict


class Hand:
    order = "AKQJT98765432"

    def __init__(self, hand: str):
        self.hand = hand

    def __eq__(self, other: "Hand") -> bool:
        return self.hand == other.hand

    def __lt__(self, other: "Hand") -> bool:
        score = self.score()
        other_score = other.score()
        if score > other_score:
            return True
        if score < other_score:
            return False
        for card, other_card in zip(self.hand, other.hand):
            if self.order.index(card) < self.order.index(other_card):
                return False
            if self.order.index(card) > self.order.index(other_card):
                return True
        return False

    def freq(self) -> dict[str, int]:
        freq = defaultdict(int)
        for card in self.hand:
            freq[card] += 1
        return freq

    def score(self) -> int:
        freq = self.freq()
        max_freq = max(freq.values())
        if max_freq == 5:
            return 0
        if max_freq == 4:
            return 1
        if max_freq == 3 and len(freq) == 2:
            return 2
        if max_freq == 3:
            return 3
        if max_freq == 2 and len(freq) == 3:
            return 4
        if max_freq == 2:
            return 5
        return 6


class JokerHand(Hand):
    order = "AKQT98765432J"

    def score(self) -> int:
        if "J" not in self.hand:
            return super().score()

        freq = self.freq()
        max_freq = max(freq.values())
        if (
            max_freq == 5
            or max_freq == freq["J"] == 4
            or max_freq == freq["J"] == 3
            or (max_freq == 3 and freq["J"] == 2)
        ):
            # JJJJJ or JJJJX or JJJXX or JJXXX or JXXXX
            return 0
        if (
            (freq["J"] == 3 and len(freq) == 3)
            or (freq["J"] == 2 and len(freq) == 3)
            or (max_freq == 3 and freq["J"] == 1)
        ):
            # JJJXY or JJXXY or JXXXY
            return 1
        if freq["J"] == 1 and len(freq) == 3 and (max_freq == 3 or max_freq == 2):
            # XXXJY or XXJYY
            return 2
        if len(freq) == 4 and freq["J"] in (1, 2):
            # XXJYZ or XJJYZ
            return 3
        return 5


def part1(content: list[str]):
    hands = []
    for line in content:
        split = line.split(" ")
        hands.append((split[0], int(split[1])))

    hands.sort(key=lambda t: Hand(t[0]))
    result = 0
    for i, hand in enumerate(hands):
        result += (i + 1) * hand[1]
    print(result)


def part2(content: list[str]):
    hands = []
    for line in content:
        split = line.split(" ")
        hands.append((split[0], int(split[1])))

    hands.sort(key=lambda t: JokerHand(t[0]))
    result = 0
    for i, hand in enumerate(hands):
        result += (i + 1) * hand[1]
    print(result)


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
    part2(content)
