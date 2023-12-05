import re


def part1(content: list[str]):
    parts = {}
    symbols = {}
    gears = {}

    for j, line in enumerate(content):
        in_part = False
        for i, char in enumerate(line):
            if "0" <= char <= "9":
                if in_part:
                    continue
                in_part = True
                number = re.match(r"^\d+", line[i:]).group(0)
                parts[(i, j)] = int(number)
                continue

            if char != ".":
                symbols[(i, j)] = True
            if char == "*":
                gears[(i, j)] = False
            in_part = False

    global_x = len(content[0])
    global_y = len(content)
    result = 0
    for pos, part in parts.items():
        min_x = max(0, pos[0] - 1)
        max_x = min(global_x - 1, pos[0] + len(str(part)))
        min_y = max(0, pos[1] - 1)
        max_y = min(global_y - 1, pos[1] + 1)
        found = False
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) in symbols:
                    found = True
        if found:
            result += part

    print(result)

    result = 0
    for pos, gear in gears.items():
        min_x = max(0, pos[0] - 1)
        max_x = min(global_x - 1, pos[0] + 1)
        min_y = max(0, pos[1] - 1)
        max_y = min(global_y - 1, pos[1] + 1)

        gear_parts = []
        for part_pos, part in parts.items():
            if part_pos[1] < min_y or part_pos[1] > max_y:
                continue
            min_part_x = part_pos[0]
            max_part_x = part_pos[0] + len(str(part)) - 1
            if (
                min_part_x <= min_x
                and max_x <= max_part_x
                or min_x <= min_part_x <= max_x
                or min_x <= max_part_x <= max_x
            ):
                gear_parts.append(part)
        if len(gear_parts) == 2:
            result += gear_parts[0] * gear_parts[1]
    print(result)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
