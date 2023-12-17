def hash(s: str) -> int:
    value = 0
    for c in s:
        value += ord(c)
        value *= 17
        value %= 256
    return value


def part1(content: str):
    result = 0
    for split in content.split(","):
        result += hash(split)
    print(result)


def part2(content: str):
    boxes = [[] for _ in range(256)]
    for split in content.split(","):
        if "=" in split:
            label, _, op = split.partition("=")
        else:
            label = split[:-1]
            op = "-"
        box_i = hash(label)
        if op == "-":
            to_remove = None
            for lens in boxes[box_i]:
                if lens[0] == label:
                    to_remove = lens
                    break
            if to_remove is not None:
                boxes[box_i].remove(to_remove)
        else:
            found = False
            for lens in boxes[box_i]:
                if lens[0] == label:
                    found = True
                    lens[1] = int(op)
            if not found:
                boxes[box_i].append([label, int(op)])

    result = 0
    for box_i, box in enumerate(boxes):
        for lens_i, lens in enumerate(box):
            result += (box_i + 1) * (lens_i + 1) * lens[1]
    print(result)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content[0])
    part2(content[0])
