import collections.abc
import sys
from collections import defaultdict

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
    unvisited = graph.nodes()

    while unvisited:
        current = unvisited[0]
        for node in unvisited:
            if distances[node] < distances[current]:
                current = node
        unvisited.remove(current)
        if cutoff and distances[current] >= cutoff:
            continue
        if end and current == end:
            break

        for node in graph.neighbors(current):
            tentative = distances[current] + graph.edge(current, node)
            if tentative < distances[node]:
                distances[node] = tentative
                previous[node] = current
    return distances, previous


def a_star_raw(
    graph: Graph,
    start: Node,
    end: Node,
    heuristic: collections.abc.Callable[[Node], int],
) -> tuple[dict[Node, int], dict[Node, Node]]:
    unvisited = [start]
    distance = defaultdict(lambda: sys.maxsize)
    distance[start] = 0
    distance_guess = defaultdict(lambda: sys.maxsize)
    distance_guess[start] = heuristic(start)
    previous = {}

    while unvisited:
        current = unvisited[0]
        for node in unvisited:
            if distance_guess[node] < distance_guess[current]:
                current = node
        if current == end:
            return distance, previous
        unvisited.remove(current)

        for node in graph.neighbors(current):
            tentative = distance[current] + graph.edge(current, node)
            if tentative < distance[node]:
                previous[node] = current
                distance[node] = tentative
                distance_guess[node] = tentative + heuristic(node)
                if node not in unvisited:
                    unvisited.append(node)
    raise ValueError(f"path from {start} to {end} not found")
