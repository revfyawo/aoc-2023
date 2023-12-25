import copy
import enum
import sys
import time
from dataclasses import dataclass
from typing import Callable

from graph import dijkstra_raw, Graph
from graph.path import reconstruct_path


class Direction(enum.Enum):
    up = "^"
    right = ">"
    down = "v"
    left = "<"

    def next(self, coord: tuple[int, int]):
        if self == Direction.up:
            return coord[0], coord[1] - 1
        if self == Direction.right:
            return coord[0] + 1, coord[1]
        if self == Direction.down:
            return coord[0], coord[1] + 1
        if self == Direction.left:
            return coord[0] - 1, coord[1]
        raise ValueError(f"invalid direction: {self}")


@dataclass
class Node:
    coord: tuple[int, int]
    direction: Direction | None
    parents: tuple[tuple[int, int], ...]

    def __hash__(self):
        return hash((self.coord, self.direction, self.parents))

    def __eq__(self, other: "Node"):
        return (
            self.coord == other.coord
            and self.direction == other.direction
            and self.parents == other.parents
        )


def part2(node: tuple[int, int]) -> list[tuple[int, int]]:
    return [
        (node[0] - 1, node[1]),
        (node[0] + 1, node[1]),
        (node[0], node[1] - 1),
        (node[0], node[1] + 1),
    ]


def part1(node: tuple[int, int]) -> list[tuple[int, int]]:
    if content[node[1]][node[0]] in ("^", ">", "v", "<"):
        return [Direction(content[node[1]][node[0]]).next(node)]
    return part2(node)


def get_path_length(
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
) -> int:
    return get_path_length_rec(
        neighbors,
        (1, 0),
        set(),
    )


def get_path_length_rec(
    neighbors: Callable[[tuple[int, int]], list[tuple[int, int]]],
    current: tuple[int, int],
    parents: set[tuple[int, int]],
) -> int:
    max_x = len(content[0]) - 1
    max_y = len(content) - 1

    def valid_neighbors(node: tuple[int, int]) -> list[tuple[int, int]]:
        return [
            neighbor
            for neighbor in neighbors(node)
            if (
                0 <= neighbor[0] <= max_x
                and 0 <= neighbor[1] <= max_y
                and content[neighbor[1]][neighbor[0]] != "#"
                and neighbor not in parents
            )
        ]

    while len(valid := valid_neighbors(current)) == 1:
        parents.add(current)
        current = valid[0]

    if current[1] == max_y:
        return len(parents)

    paths = []
    for neighbor in neighbors(current):
        if not (0 <= neighbor[0] <= max_x and 0 <= neighbor[1] <= max_y):
            continue

        next_value = content[neighbor[1]][neighbor[0]]
        if next_value != "#" and neighbor not in parents:
            paths.append(
                get_path_length_rec(
                    neighbors,
                    neighbor,
                    parents | {current},
                )
            )

    if not paths:
        return 0
    return max(paths)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]

    for neighbor in (part1, part2):
        start_time = time.perf_counter()
        start = Node((0, 1), None, ())
        result = get_path_length(neighbor)
        end_time = time.perf_counter()
        print(f"took {end_time-start_time:.3}s")
        print(result)
