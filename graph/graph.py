import collections
import typing

Node = typing.TypeVar("Node", bound=collections.abc.Hashable)


class Graph(typing.Generic[Node]):
    def __init__(self):
        self._nodes: dict[Node, dict[Node, int]] = {}

    def add_node(self, node: Node):
        if node not in self._nodes:
            self._nodes[node] = {}

    def add_edge(self, start: Node, end: Node, weight=1):
        self._nodes[start][end] = weight

    def nodes(self) -> list[Node]:
        return list(self._nodes.keys())

    def neighbors(self, node: Node) -> list[Node]:
        return list(self._nodes[node].keys())

    def edge(self, start: Node, end: Node) -> int:
        return self._nodes[start][end]
