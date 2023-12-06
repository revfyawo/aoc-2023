import functools
from operator import attrgetter


@functools.total_ordering
class Interval:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length

    def __str__(self):
        return f"[{self.start}, {self.start+self.length-1}]"

    def __repr__(self):
        return f"Interval({self.start}, {self.length})"

    def __contains__(self, item):
        return self.start <= item < self.start + self.length

    def __and__(self, other: "Interval") -> "Interval":
        if self.empty or other.empty:
            return Interval(0, 0)

        if self.start <= other.start <= self.end:
            return Interval(other.start, min(self.end, other.end) - other.start + 1)
        if self.start <= other.end <= self.end:
            start = max(self.start, other.start)
            return Interval(start, other.end - start + 1)
        if other.start <= self.start and self.end <= other.end:
            return self

        return Interval(0, 0)

    def __eq__(self, other: "Interval") -> bool:
        if self.empty and other.empty:
            return True
        return self.start == other.start and self.end == other.end

    def __le__(self, other: "Interval") -> bool:
        if self.empty:
            return True
        return other.start <= self.start and self.end <= other.end

    def __hash__(self):
        return hash(range(self.start, self.start + self.length))

    @property
    def end(self):
        return self.start + self.length - 1

    @property
    def empty(self):
        return self.length <= 0

    def copy(self) -> "Interval":
        return Interval(self.start, self.length)

    def intersection(self, *others: "Interval") -> "Interval":
        copy = self.copy()
        for other in others:
            copy &= other
        return copy


class IntervalMap:
    def __init__(self):
        self._map = {}

    def __repr__(self):
        sorted_keys = sorted(self._map.keys(), key=attrgetter("start"))
        return (
            "IntervalMap("
            + ", ".join([f"{src} => {self._map[src]}" for src in sorted_keys])
            + ")"
        )

    def copy(self):
        copy = IntervalMap()
        copy._map = {src.copy(): dest.copy() for src, dest in self._map.items()}
        return copy

    def add_interval(self, src: int, dest: int, length: int):
        self._map[Interval(src, length)] = Interval(dest, length)

    def map(self, value: int) -> int:
        for start, dest in self._map.items():
            if value in start:
                return dest.start + value - start.start
        return value

    def map_intervals(self, *intervals: Interval) -> list[Interval]:
        outputs = []
        for interval in intervals:
            found = False
            for src, dest in self._map.items():
                intersection = interval.intersection(src)
                if intersection.empty:
                    continue
            # TODO
            if not found:
                outputs.append(interval.copy())
        return outputs


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
    with open("./example.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
