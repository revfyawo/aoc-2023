import enum


class Direction(enum.Enum):
    up = "^"
    right = ">"
    down = "v"
    left = "<"

    def next_pos(self, pos: tuple[int, int]) -> tuple[int, int]:
        if self == Direction.up:
            return pos[0], pos[1] - 1
        if self == Direction.right:
            return pos[0] + 1, pos[1]
        if self == Direction.down:
            return pos[0], pos[1] + 1
        if self == Direction.left:
            return pos[0] - 1, pos[1]
        raise RuntimeError(f"invalid self value {self}")


def let_there_be_light(
    content: list[str], start: tuple[tuple[int, int], Direction]
) -> int:
    max_x = len(content)
    max_y = len(content[0])
    energized = [[False for _ in range(max_y)] for _ in range(max_x)]
    beams = [start]
    done = set()

    while beams:
        beam = beams.pop()
        pos = beam[0]
        if beam in done or not (0 <= pos[0] < max_x and 0 <= pos[1] < max_y):
            # Simpler OOB check done here than in all cases
            continue

        done.add(beam)
        energized[pos[1]][pos[0]] = True
        direction = beam[1]
        current = content[pos[1]][pos[0]]
        if current == ".":
            beams.append((direction.next_pos(pos), direction))
        elif current in ("/", "\\"):
            if current == "/":
                if direction == Direction.up:
                    next_direction = Direction.right
                elif direction == Direction.right:
                    next_direction = Direction.up
                elif direction == Direction.down:
                    next_direction = Direction.left
                else:
                    next_direction = Direction.down
            else:
                if direction == Direction.up:
                    next_direction = Direction.left
                elif direction == Direction.right:
                    next_direction = Direction.down
                elif direction == Direction.down:
                    next_direction = Direction.right
                else:
                    next_direction = Direction.up
            beams.append((next_direction.next_pos(pos), next_direction))
        elif current in ("|", "-"):
            next_directions = []
            if current == "|":
                if direction in (Direction.up, Direction.down):
                    next_directions.append(direction)
                else:
                    next_directions.append(Direction.up)
                    next_directions.append(Direction.down)
            else:
                if direction in (Direction.left, Direction.right):
                    next_directions.append(direction)
                else:
                    next_directions.append(Direction.left)
                    next_directions.append(Direction.right)
            for next_direction in next_directions:
                beams.append((next_direction.next_pos(pos), next_direction))

    total = 0
    for line in energized:
        for pos in line:
            if pos:
                total += 1
    return total


def part1(content: list[str]):
    total = let_there_be_light(content, ((0, 0), Direction.right))
    print(total)


def part2(content: list[str]):
    total = None
    max_x = len(content)
    max_y = len(content[0])
    for i in range(max_x):
        attempt = let_there_be_light(content, ((i, 0), Direction.down))
        if total is None or attempt > total:
            total = attempt
        attempt = let_there_be_light(content, ((i, max_y - 1), Direction.up))
        if total is None or attempt > total:
            total = attempt
    for i in range(max_y):
        attempt = let_there_be_light(content, ((0, i), Direction.right))
        if total is None or attempt > total:
            total = attempt
        attempt = let_there_be_light(content, ((max_x - 1, i), Direction.left))
        if total is None or attempt > total:
            total = attempt
    print(total)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]
    part1(content)
    part2(content)
