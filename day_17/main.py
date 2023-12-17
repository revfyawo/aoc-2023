Node = tuple[int, int]


class World:
    def __init__(self, nodes: dict[Node, int]):
        self.nodes = nodes
        self.max_x, self.max_y = 0, 0
        for node in nodes:
            if node[0] > self.max_x:
                self.max_x = node[0]
            if node[1] > self.max_y:
                self.max_y = node[1]

    def neighbors(self, node: Node, previous: dict[Node, Node]) -> list[Node]:
        path = get_path(node, previous)
        direction = get_direction_string(path)
        direction = "".join(reversed(direction))
        if not direction:
            direction = "   "

        neighbors = []
        if node[1] > 0 and direction[0] != "v" and direction[:3] != "^^^":
            neighbors.append((node[0], node[1] - 1))
        if node[0] < self.max_x and direction[0] != "<" and direction[:3] != ">>>":
            neighbors.append((node[0] + 1, node[1]))
        if node[1] < self.max_y and direction[0] != "^" and direction[:3] != "vvv":
            neighbors.append((node[0], node[1] + 1))
        if node[0] > 0 and direction[0] != ">" and direction[:3] != "<<<":
            neighbors.append((node[0] - 1, node[1]))
        return neighbors

    def path_weight(self, path: list[Node]) -> int:
        weight = 0
        for node in path[1:]:
            weight += self.nodes[node]
        return weight

    def print_path(self, path: list[Node]):
        world = [
            [str(self.nodes[(i, j)]) for i in range(self.max_x + 1)]
            for j in range(self.max_y + 1)
        ]
        for current, next in zip(path, path[1:]):
            world[current[1]][current[0]] = get_direction_string([current, next])
        world[path[-1][1]][path[-1][0]] = "X"
        for line in world:
            print("".join(line))


def get_direction_string(path: list[Node]) -> str:
    direction = ""
    for current, next in zip(path, path[1:]):
        if next[0] > current[0]:
            direction += ">"
        elif next[0] < current[0]:
            direction += "<"
        elif next[1] > current[1]:
            direction += "v"
        else:
            direction += "^"
    return direction


def a_star(world: World) -> list[Node]:
    start = (0, 0)
    end = (world.max_x, world.max_y)

    previous = {}
    shortest = {start: 0}
    estimate = {start: world.max_x + world.max_y}
    open_set = {start}

    while open_set:
        current = None
        for node in open_set:
            if node in estimate and (
                current is None or estimate[node] < estimate[current]
            ):
                current = node
        if current == end:
            return get_path(current, previous)

        open_set.remove(current)
        neighbors = world.neighbors(current, previous)
        for neighbor in neighbors:
            tentative = shortest[current] + world.nodes[neighbor]
            if neighbor not in shortest or tentative < shortest[neighbor]:
                previous[neighbor] = current
                shortest[neighbor] = tentative
                estimate[neighbor] = (
                    tentative + abs(end[0] - neighbor[0]) + abs(end[1] - neighbor[1])
                )
                open_set.add(neighbor)

    raise RuntimeError("end not found")


def get_path(current: Node, previous: dict[Node, Node]) -> list[Node]:
    path = [current]
    while current in previous:
        current = previous[current]
        path.append(current)
    path.reverse()
    return path


def part1(world: World):
    path = a_star(world)
    world.print_path(path)
    print(world.path_weight(path))


if __name__ == "__main__":
    with open("example.txt") as f:
        content = f.read().split("\n")[:-1]

    nodes = {}
    for j, line in enumerate(content):
        for i, char in enumerate(line):
            nodes[(i, j)] = int(char)
    world = World(nodes)
    part1(world)
