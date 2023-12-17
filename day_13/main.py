def split_patterns(content: list[str]) -> list[list[list[bool]]]:
    pattern_count = content.count("") + 1

    delimiters = []
    last_delimiter = -1
    for i in range(pattern_count - 1):
        delimiter = content.index("", last_delimiter + 1)
        delimiters.append(delimiter)
        last_delimiter = delimiter

    patterns = []
    for i in range(pattern_count):
        if i == 0:
            start = 0
        else:
            start = delimiters[i - 1] + 1
        if i == pattern_count - 1:
            stop = len(content)
        else:
            stop = delimiters[i]

        pattern = []
        for line in content[start:stop]:
            pattern.append([c == "#" for c in line])
        patterns.append(pattern)
    return patterns


def check_row_symmetry(pattern: list[list[bool]], row: int) -> bool:
    row_count = len(pattern)
    for i in range(min(row + 1, row_count - row - 1)):
        if pattern[row - i] != pattern[row + 1 + i]:
            return False
    return True


def check_column_symmetry(pattern: list[list[bool]], col: int) -> bool:
    columns = [[row[i] for row in pattern] for i in range(len(pattern[0]))]
    col_count = len(columns)
    for i in range(min(col + 1, col_count - col - 1)):
        if columns[col - i] != columns[col + 1 + i]:
            return False
    return True


def part1(patterns: list[list[list[bool]]]):
    result = 0
    for pattern in patterns:
        for row in range(len(pattern) - 1):
            if check_row_symmetry(pattern, row):
                result += 100 * (row + 1)
        for col in range(len(pattern[0]) - 1):
            if check_column_symmetry(pattern, col):
                result += col + 1
    print(result)


def part2(patterns: list[list[list[bool]]]):
    result = 0
    for pattern in patterns:
        base_row = None
        base_col = None
        for row in range(len(pattern) - 1):
            if check_row_symmetry(pattern, row):
                base_row = row
                break
        for col in range(len(pattern[0]) - 1):
            if check_column_symmetry(pattern, col):
                base_col = col
                break

        smudge_found = False
        for i in range(len(pattern)):
            for j in range(len(pattern[0])):
                pattern[i][j] = not pattern[i][j]
                for row in range(len(pattern) - 1):
                    if row != base_row and check_row_symmetry(pattern, row):
                        result += 100 * (row + 1)
                        smudge_found = True
                for col in range(len(pattern[0]) - 1):
                    if col != base_col and check_column_symmetry(pattern, col):
                        result += col + 1
                        smudge_found = True
                pattern[i][j] = not pattern[i][j]
                if smudge_found:
                    break
            if smudge_found:
                break
    print(result)


if __name__ == "__main__":
    with open("input.txt") as f:
        content = f.read().split("\n")[:-1]
    patterns = split_patterns(content)
    part1(patterns)
    part2(patterns)
