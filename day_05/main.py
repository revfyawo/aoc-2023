def parse_range_map(lines: list[str]) -> list[dict]:
    result = []
    for line in lines:
        split = line.split(" ")
        result.append(
            {"len": int(split[2]), "src": int(split[1]), "dest": int(split[0])}
        )
    return result


def part1(content: list[str]):
    seeds = map(int, content[0].split(": ")[1].split(" "))

    maps = []
    map_stop = 1
    for _ in range(7):
        map_start = map_stop + 2
        try:
            map_stop = content[map_start:].index("") + map_start
        except ValueError:
            map_stop = len(content)
        maps.append(parse_range_map(content[map_start:map_stop]))

    locations = []
    for seed in seeds:
        location = seed
        for i, map_ in enumerate(maps):
            for range_ in map_:
                if location in range(range_["src"], range_["src"] + range_["len"]):
                    location = range_["dest"] + location - range_["src"]
                    break
        locations.append(location)

    print(min(locations))


def part2(content: list[str]):
    pass


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
