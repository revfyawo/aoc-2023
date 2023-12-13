import copy
import math


def dijkstra(galaxies: list[tuple[int, int]]) -> dict[tuple[int, int], int]:
    source = galaxies[0]
    unvisited = []
    distances = {}
    previous = {}
    for galaxy in galaxies:
        distances[galaxy] = math.inf
        previous[galaxy] = None
        unvisited.append(galaxy)
    distances[source] = 0

    while unvisited:
        min_distance = None
        for galaxy in unvisited:
            if min_distance is None or distances[galaxy] < distances[min_distance]:
                min_distance = galaxy
        unvisited.remove(min_distance)
        for neighbor in unvisited:
            alt = (
                distances[min_distance]
                + abs(neighbor[0] - source[0])
                + abs(neighbor[1] - source[1])
            )
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = min_distance
    return distances


def expand(
    content: list[str],
    galaxies: list[tuple[int, int]],
    factor: int,
):
    j = 0
    for row in content:
        if all((char == "." for char in row)):
            for gal_i, galaxy in enumerate(galaxies):
                if galaxy[1] > j:
                    galaxies[gal_i] = (galaxy[0], galaxy[1] + factor)
            j += factor
        j += 1

    i = 0
    for column in [
        "".join([line[i] for line in content]) for i in range(len(content[0]))
    ]:
        if all((char == "." for char in column)):
            for gal_i, galaxy in enumerate(galaxies):
                if galaxy[0] > i:
                    galaxies[gal_i] = (galaxy[0] + factor, galaxy[1])
            i += factor
        i += 1


def problem(galaxies: list[tuple[int, int]], expansion_factor: int):
    expand(content, galaxies, expansion_factor)
    paths = {}
    for i in range(len(galaxies)):
        slice_paths = dijkstra(galaxies[i:])
        for dest, dist in slice_paths.items():
            paths[(galaxies[i], dest)] = dist

    print(sum(paths.values()))


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]

    galaxies = []
    for j, line in enumerate(content):
        for i, char in enumerate(line):
            if char == "#":
                galaxies.append((i, j))

    problem(copy.copy(galaxies), 1)
    problem(copy.copy(galaxies), 999999)
