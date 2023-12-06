class Interval:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length

    def __contains__(self, item):
        return self.start <= item < self.start + self.length


class IntervalMap:
    def __init__(self):
        self._map = {}

    def add_interval(self, src: int, dest: int, length: int):
        self._map[Interval(src, length)] = Interval(dest, length)

    def map(self, value: int) -> int:
        for start, dest in self._map.items():
            if value in start:
                return dest.start + value - start.start
        return value


def parse_range_map(lines: list[str]) -> IntervalMap:
    imap = IntervalMap()
    for line in lines:
        split = line.split(" ")
        imap.add_interval(int(split[1]), int(split[0]), int(split[2]))
    return imap


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
        for i, imap in enumerate(maps):
            location = imap.map(location)
        locations.append(location)

    print(min(locations))


def part2(content: list[str]):
    pass


if __name__ == "__main__":
    with open("./input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
