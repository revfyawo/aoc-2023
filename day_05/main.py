from functools import total_ordering
from operator import attrgetter


@total_ordering
class Interval:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length

    def __str__(self):
        return f"[{self.start}, {self.start+self.length-1}]"

    def __repr__(self):
        return f"Interval({self.start}, {self.length})"

    def __contains__(self, item):
        return self.start <= item <= self.end

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

    def split_disjoint(self, other: "Interval") -> list["Interval"]:
        if self.intersection(other).empty:
            return []
        if self == other:
            return [self.copy()]

        if self.start == other.start:
            cutoffs = [
                self.start,
                min(self.end, other.end) + 1,
                max(self.end, other.end) + 1,
            ]
        else:
            cutoffs = [min(self.start, other.start), max(self.start, other.start)]
            if self.end == other.end:
                cutoffs.append(self.end + 1)
            else:
                cutoffs.extend(
                    [min(self.end, other.end) + 1, max(self.end, other.end) + 1]
                )

        split = [Interval(cutoffs[0], cutoffs[1] - cutoffs[0])]
        for i in range(1, len(cutoffs) - 1):
            split.append(Interval(cutoffs[i], cutoffs[i + 1] - cutoffs[i]))
        return split

    def split_by(self, other: "Interval") -> list["Interval"]:
        split = self.split_disjoint(other)
        if not split:
            return split

        split_contained = []
        for interval in split:
            if interval <= self:
                split_contained.append(interval)
        return split_contained


class IntervalMap:
    def __init__(self):
        self._map: dict[Interval, Interval] = {}

    def __repr__(self):
        sorted_keys = sorted(self._map.keys(), key=attrgetter("start"))
        return (
            "IntervalMap("
            + ", ".join([f"{src} => {self._map[src]}" for src in sorted_keys])
            + ")"
        )

    def add_interval(self, src: int, dest: int, length: int):
        self._map[Interval(src, length)] = Interval(dest, length)

    def map(self, value: int) -> int:
        for start, dest in self._map.items():
            if value in start:
                return dest.start + value - start.start
        return value

    def copy(self):
        copy = IntervalMap()
        copy._map = {src.copy(): dest.copy() for src, dest in self._map.items()}
        return copy

    def split_interval(self, src, intervals):
        new_dests = [
            Interval(self.map(interval.start), interval.length)
            for interval in intervals
        ]
        del self._map[src]
        for src, dest in zip(intervals, new_dests):
            self.add_interval(src.start, dest.start, src.length)

    def merge(self, other: "IntervalMap") -> "IntervalMap":
        to_split_self = {}  # maps self old src to new dests
        to_split_other = {}  # maps other old src to new srcs
        for other_src in other._map.keys():
            for src, dest in self._map.items():
                if dest.intersection(other_src).empty or dest == other_src:
                    continue

                split_other = other_src.split_by(dest)
                if len(split_other) > 1:
                    to_split_other[other_src] = split_other
                new_dests = dest.split_by(other_src)
                if len(new_dests) > 1:
                    new_srcs = []
                    consumed = 0
                    for dest in new_dests:
                        new_srcs.append(Interval(src.start + consumed, dest.length))
                        consumed += dest.length
                    to_split_self[src] = new_srcs

        self_copy = self.copy()
        for old_src, new_srcs in to_split_self.items():
            self_copy.split_interval(old_src, new_srcs)
        print(f"split self {self} in {self_copy}")

        other_copy = other.copy()
        for old_src, new_srcs in to_split_other.items():
            other_copy.split_interval(old_src, new_srcs)
        print(f"split other {other} in {other_copy}")

        for other_src, other_dest in other_copy._map.items():
            if other_src not in self_copy._map.values():
                self_copy._map[other_src] = other_dest

        for src, dest in self_copy._map.items():
            for other_src, other_dest in other_copy._map.items():
                if dest == other_src:
                    self_copy._map[src] = other_dest

        print(f"merged {other} in {self}: {self_copy}")

        for i in range(100):
            print(f"{i:02}", end=" ")
        print()
        for i in range(100):
            print(f"{self.map(i):02}", end=" ")
        print()
        for i in range(100):
            print(f"{other.map(self.map(i)):02}", end=" ")
        print()
        for i in range(100):
            print(f"{self_copy.map(i):02}", end=" ")
        print()

        return self_copy


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

    print(maps)
    global_map = maps[0].copy()
    for imap in maps[1:]:
        global_map = global_map.merge(imap)

    locations = []
    for seed in seeds:
        locations.append(global_map.map(seed))

    print(min(locations))


def part2(content: list[str]):
    pass


if __name__ == "__main__":
    with open("./example.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
