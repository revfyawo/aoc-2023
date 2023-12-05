def part1():
    with open("./example.txt") as f:
        content = f.read()

    values = []
    for line in content.split("\n"):
        first, last = None, None
        for char in line:
            if "0" <= char <= "9":
                if first is None:
                    first = char
                last = char
        if first is not None:
            values.append(int(first) * 10 + int(last))
    print(sum(values))


def part2():
    with open("./input.txt") as f:
        content = f.read()

    values = []
    for line in content.split("\n"):
        first, last = None, None
        first_i, last_i = None, None
        for i, char in enumerate(line):
            if "0" <= char <= "9":
                if first is None:
                    first = int(char)
                    first_i = i
                last = int(char)
                last_i = i

        for number_i, number_c in enumerate(
            ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        ):
            for i in (line.find(number_c), line.rfind(number_c)):
                if i == -1:
                    continue

                if first_i is None or i < first_i:
                    first = number_i + 1
                    first_i = i
                if last_i is None or i > last_i:
                    last = number_i + 1
                    last_i = i

        if first is not None:
            value = first * 10 + last
            values.append(value)

    print(sum(values))


if __name__ == "__main__":
    part1()
    part2()
