import re


def race(time, to_beat) -> int:
    possible = []
    for j in range(time + 1):
        possible.append(j * (time - j))
    return len(list(filter(lambda x: x > to_beat, possible)))


def part1(content: list[str]):
    times = list(map(int, re.findall(r"\d+", content[0])))
    distances = list(map(int, re.findall(r"\d+", content[1])))
    result = 1
    for time, distance in zip(times, distances):
        result *= race(time, distance)
    print(result)


def part2(content: list[str]):
    times = list(map(int, re.findall(r"\d+", content[0].replace(" ", ""))))
    distances = list(map(int, re.findall(r"\d+", content[1].replace(" ", ""))))
    result = 1
    for time, distance in zip(times, distances):
        result *= race(time, distance)
    print(result)


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
    part2(content)
