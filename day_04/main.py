import re


def part1(cards: list[tuple[list, list]]):
    result = 0
    for winning, numbers in cards:
        wins = 0
        for number in numbers:
            if number in winning:
                wins += 1

        if wins:
            result += 1 << (wins - 1)
    print(result)


def part2(cards: list[tuple[list, list]]):
    copies = [1 for _ in range(len(cards))]
    for i, (winning, numbers) in enumerate(cards):
        wins = 0
        for number in numbers:
            if number in winning:
                wins += 1
        if wins:
            for j in range(min(i + 1, len(copies)), min(i + wins + 1, len(copies))):
                copies[j] += copies[i]

    print(sum(copies))


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    cards = []
    for line in content:
        winning_numbers = re.findall(r"\d+", line.split(":")[1].split("|")[0])
        card_numbers = re.findall(r"\d+", line.split(":")[1].split("|")[1])
        cards.append((winning_numbers, card_numbers))

    part1(cards)
    part2(cards)
