import collections.abc
import sys
from collections import defaultdict, deque
from heapq import heappop, heappush

from .graph import Graph, Node


def dijkstra_raw(
    graph: Graph[Node],
    start: Node,
    end: Node | None = None,
    cutoff: int | None = None,
) -> tuple[dict[Node, int], dict[Node, Node]]:
    distances = defaultdict(lambda: sys.maxsize)
    distances[start] = 0
    previous = {}

    queue = [(distances[start], 0, start)]
    visited = set()

    tie_breaker = 1
    while queue:
        _, _, current = heappop(queue)
        visited.add(current)
        if cutoff and distances[current] >= cutoff:
            continue
        if end and current == end:
            break

        for node in graph.neighbors(current):
            if node in visited:
                continue

            tentative = distances[current] + graph.edge(current, node)
            if tentative < distances[node]:
                distances[node] = tentative
                previous[node] = current
                heappush(queue, (distances[node], tie_breaker, node))
                tie_breaker += 1
    return distances, previous


def a_star_raw(
    graph: Graph,
    start: Node,
    end: Node,
    heuristic: collections.abc.Callable[[Node], int],
) -> tuple[dict[Node, int], dict[Node, Node]]:
    distance = defaultdict(lambda: sys.maxsize)
    distance[start] = 0
    distance_guess = defaultdict(lambda: sys.maxsize)
    distance_guess[start] = heuristic(start)
    previous = {}

    unvisited = [(0, 0, start)]
    visited = set()

    tie_breaker = 1
    while unvisited:
        _, _, current = heappop(unvisited)
        if current == end:
            return distance, previous
        visited.add(current)

        for node in graph.neighbors(current):
            if node in visited:
                continue

            tentative = distance[current] + graph.edge(current, node)
            if tentative < distance[node]:
                previous[node] = current
                distance[node] = tentative
                distance_guess[node] = tentative + heuristic(node)
                heappush(unvisited, (distance[node], tie_breaker, node))
                tie_breaker += 1

    raise ValueError(f"path from {start} to {end} not found")


def reconstruct_path(end_node: Node, previous: dict[Node, Node]) -> list[Node]:
    current = end_node
    path = deque([current])
    while current in previous:
        current = previous[current]
        path.appendleft(current)
    return list(path)
