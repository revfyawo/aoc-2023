import sys
from collections import defaultdict

Node = tuple[int, int]


class Graph:
    def __init__(self, content: list[str]):
        self.plots = set()

        for j, line in enumerate(content):
            for i, char in enumerate(line):
                if char == "S":
                    self.root = i, j
                    self.plots.add((i, j))
                elif char == ".":
                    self.plots.add((i, j))

    def nodes(self) -> list[Node]:
        return list(self.plots)

    def distance(self, start: Node, end: Node) -> int:
        if end not in self.neighbors(start):
            raise ValueError(f"{end} not in {start} neighbors")
        return 1

    def neighbors(self, node: Node) -> list[Node]:
        neighbors = []
        for i in (node[0] - 1, node[0] + 1):
            if (i, node[1]) in self.plots:
                neighbors.append((i, node[1]))
        for j in (node[1] - 1, node[1] + 1):
            if (node[0], j) in self.plots:
                neighbors.append((node[0], j))
        return neighbors


def dijkstra(
    graph: Graph, start: Node, cutoff: int | None = None
) -> tuple[dict[Node, int], dict[Node, Node]]:
    distance = defaultdict(lambda: sys.maxsize)
    distance[start] = 0
    previous = {}
    unvisited = graph.nodes()

    while unvisited:
        current = unvisited[0]
        for node in unvisited:
            if distance[node] < distance[current]:
                current = node
        unvisited.remove(current)
        if cutoff and distance[current] >= cutoff:
            continue

        for node in graph.neighbors(current):
            if node not in unvisited:
                continue
            tentative = distance[current] + graph.distance(current, node)
            if node not in distance or tentative < distance[node]:
                distance[node] = tentative
                previous[node] = current

    return distance, previous


def part1(graph: Graph, steps: int):
    distance, previous = dijkstra(graph, graph.root, steps)
    result = 0
    for node, dist in distance.items():
        if dist <= steps and dist % 2 == 0:
            result += 1
    print(result)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]
    graph = Graph(content)
    part1(graph, 64)
