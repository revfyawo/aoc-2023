import re
from collections import defaultdict
from functools import reduce


def part1(content: list[str]):
    result = 0
    max_possible = {"red": 12, "green": 13, "blue": 14}
    for game in content:
        possible = True
        game_id, _, hands = game.partition(": ")
        game_id = re.match(r"^Game (\d+)$", game_id).group(1)
        for hand in hands.split("; "):
            for color in hand.split(", "):
                number, color = color.split(" ")
                if int(number) > max_possible[color]:
                    possible = False
        if possible:
            result += int(game_id)
    print(result)


def part2(content: list[str]):
    result = 0
    for game in content:
        max_possible = defaultdict(int)
        _, _, hands = game.partition(": ")
        for hand in hands.split("; "):
            for color in hand.split(", "):
                number, color = color.split(" ")
                if int(number) > max_possible[color]:
                    max_possible[color] = int(number)
        result += reduce(lambda acc, val: acc * val, max_possible.values(), 1)
    print(result)


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
    part2(content)
