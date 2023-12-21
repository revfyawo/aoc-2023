import enum
import time
from collections import namedtuple

from graph import a_star_raw, dijkstra_raw, Graph


class Direction(enum.Enum):
    up = "^"
    down = "v"
    left = "<"
    right = ">"

    def next(self, coords: tuple[int, int]) -> tuple[int, int]:
        if self == Direction.up:
            return coords[0], coords[1] - 1
        if self == Direction.down:
            return coords[0], coords[1] + 1
        if self == Direction.left:
            return coords[0] - 1, coords[1]
        if self == Direction.right:
            return coords[0] + 1, coords[1]
        raise ValueError(f"value {self} is not a direction")


Node = namedtuple("Node", ["coords", "direction"])


def print_path(content: list[str], path: list[Node]):
    world = [["." for char in line] for line in content]
    for node, next_node in zip(path, path[1:]):
        world[node.coords[1]][node.coords[0]] = next_node.direction.value
    for line in world:
        print("".join(line))


def part1_graph(content: list[str]) -> Graph:
    graph: Graph[Node] = Graph()
    coord_values = {}
    for j, line in enumerate(content):
        for i, char in enumerate(line):
            value = int(char)
            coord_values[(i, j)] = value
            graph.add_node(Node((i, j), Direction.up))
            graph.add_node(Node((i, j), Direction.down))
            graph.add_node(Node((i, j), Direction.left))
            graph.add_node(Node((i, j), Direction.right))

    for node in graph.nodes():
        orthogonal = {
            Direction.up: [Direction.left, Direction.right],
            Direction.down: [Direction.left, Direction.right],
            Direction.left: [Direction.up, Direction.down],
            Direction.right: [Direction.up, Direction.down],
        }
        for direction in orthogonal[node.direction]:
            cumsum = 0
            current = node.coords
            for _ in range(3):
                current = direction.next(current)
                if current not in coord_values:
                    continue
                cumsum += coord_values[current]
                graph.add_edge(node, Node(current, direction), weight=cumsum)
    return graph


def part2_graph(content: list[str]) -> Graph:
    graph: Graph[Node] = Graph()
    coord_values = {}
    for j, line in enumerate(content):
        for i, char in enumerate(line):
            value = int(char)
            coord_values[(i, j)] = value
            graph.add_node(Node((i, j), Direction.up))
            graph.add_node(Node((i, j), Direction.down))
            graph.add_node(Node((i, j), Direction.left))
            graph.add_node(Node((i, j), Direction.right))

    for node in graph.nodes():
        orthogonal = {
            Direction.up: [Direction.left, Direction.right],
            Direction.down: [Direction.left, Direction.right],
            Direction.left: [Direction.up, Direction.down],
            Direction.right: [Direction.up, Direction.down],
        }
        for direction in orthogonal[node.direction]:
            cumsum = 0
            current = node.coords
            oob = False
            for _ in range(3):
                current = direction.next(current)
                if current not in coord_values:
                    oob = True
                    break
                cumsum += coord_values[current]
            if oob:
                continue
            for _ in range(7):
                current = direction.next(current)
                if current not in coord_values:
                    break
                cumsum += coord_values[current]
                graph.add_edge(node, Node(current, direction), weight=cumsum)
    return graph


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]

    max_x = len(content[0]) - 1
    max_y = len(content) - 1
    end_nodes = [
        Node((max_x, max_y), Direction.right),
        Node((max_x, max_y), Direction.down),
    ]

    graph = part1_graph(content)
    distances, _ = dijkstra_raw(graph, Node((0, 0), Direction.right))
    print(min(distances[end_nodes[0]], distances[end_nodes[1]]))

    graph = part2_graph(content)
    distances, _ = dijkstra_raw(graph, Node((0, 0), Direction.right))
    print(min(distances[end_nodes[0]], distances[end_nodes[1]]))
