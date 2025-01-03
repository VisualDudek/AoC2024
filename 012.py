from collections import defaultdict
from itertools import count
from typing import List, Set, Tuple

MAX_X: int = 0
MAX_Y: int = 0

test_data = """AAAA
BBCD
BBCC
EEEC"""

test_data_02 = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

test_data_03 = """AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA"""

test_data_04 = """AAAA
BBCD
BBCC
EEEC"""

test_data_05 = """EEEEE
EXXXX
EEEEE
EXXXX
EEEEE"""


def parse_data(s: str) -> defaultdict[Tuple[int, int], str]:
    """
    Parse the data into a dictionary of (x, y) -> value.
    """
    lines = s.split("\n")
    global MAX_X, MAX_Y
    MAX_X = len(lines[0])
    MAX_Y = len(lines)

    data: defaultdict[Tuple[int, int], str] = defaultdict(str)

    for x in range(MAX_X):
        for y in range(MAX_Y):
            data[(x, y)] = lines[y][x]

    return data


def traverse_mattrix(d: defaultdict[Tuple[int, int], str]):
    visited_set: Set[Tuple[int, int]] = set()
    groups: defaultdict[int, List[Tuple[int, int]]] = defaultdict(list)
    counter = count()

    for y in range(MAX_Y):
        for x in range(MAX_X):
            if (x, y) not in visited_set:
                id = next(counter)
                find_group(
                    d,
                    x,
                    y,
                    groups[id],
                    d[(x, y)],
                    visited_set,
                )

    return groups


def find_group(
    d: defaultdict[Tuple[int, int], str],
    x: int,
    y: int,
    groups: List[Tuple[int, int]],
    c: str,
    visited_set: Set[Tuple[int, int]],
) -> None:
    if (x, y) not in visited_set and d[(x, y)] == c:
        groups.append((x, y))
        visited_set.add((x, y))
        find_group(d, x + 1, y, groups, c, visited_set)
        find_group(d, x - 1, y, groups, c, visited_set)
        find_group(d, x, y + 1, groups, c, visited_set)
        find_group(d, x, y - 1, groups, c, visited_set)
    pass


def calculate_part_one(groups: defaultdict[int, List[Tuple[int, int]]]) -> int:
    res = 0
    for _, group in groups.items():
        # calculate perimeter
        perimeter = 0
        for item in group:
            x, y = item
            # Check all four sides
            if (x + 1, y) not in group:
                perimeter += 1
            if (x - 1, y) not in group:
                perimeter += 1
            if (x, y + 1) not in group:
                perimeter += 1
            if (x, y - 1) not in group:
                perimeter += 1
        res += perimeter * len(group)

    return res


def calculate_part_two(groups: defaultdict[int, List[Tuple[int, int]]]) -> int:
    res = 0
    for _, group in groups.items():
        # calculate number of edges
        edges = 0
        visited_set: Set[
            Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]
        ] = set()
        for item in group:
            x, y = item
            # Check all four sides
            # left up
            corner = ((x - 1, y - 1), (x, y - 1), (x - 1, y), (x, y))
            if is_corner(corner, group) and corner not in visited_set:
                visited_set.add(corner)
                if is_corner_double(corner, group):
                    edges += 2
                else:
                    edges += 1
            # right up
            corner = ((x, y - 1), (x + 1, y - 1), (x, y), (x + 1, y))
            if is_corner(corner, group) and corner not in visited_set:
                visited_set.add(corner)
                if is_corner_double(corner, group):
                    edges += 2
                else:
                    edges += 1

            # left down
            corner = ((x - 1, y), (x, y), (x - 1, y + 1), (x, y + 1))
            if is_corner(corner, group) and corner not in visited_set:
                visited_set.add(corner)
                if is_corner_double(corner, group):
                    edges += 2
                else:
                    edges += 1

            # right down
            corner = ((x, y), (x + 1, y), (x, y + 1), (x + 1, y + 1))
            if is_corner(corner, group) and corner not in visited_set:
                visited_set.add(corner)
                if is_corner_double(corner, group):
                    edges += 2
                else:
                    edges += 1

        res += edges * len(group)
        # print(f"group: {group} edges: {edges}")
        # print(f"visited_set: {visited_set}")

    return res


def is_corner(
    corner: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]],
    group: List[Tuple[int, int]],
) -> bool:
    LU, RU, LD, RD = corner
    if LU in group and RU in group and LD not in group and RD not in group:
        return False
    if LU not in group and RU in group and LD not in group and RD in group:
        return False
    if LU not in group and RU not in group and LD in group and RD in group:
        return False
    if LU in group and RU not in group and LD in group and RD not in group:
        return False
    if LU in group and RU in group and LD in group and RD in group:
        return False
    return True


def is_corner_double(
    corner: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]],
    group: List[Tuple[int, int]],
) -> bool:
    LU, RU, LD, RD = corner
    if LU in group and RD in group and RU not in group and LD not in group:
        return True
    if LU not in group and RD not in group and RU in group and LD in group:
        return True
    return False


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def test():
    # data = parse_data(test_data)
    # data = parse_data(test_data_02)
    data = parse_data(test_data_03)
    data = parse_data(get_file_data("./data/012.txt"))
    print(data)
    gr = traverse_mattrix(data)
    print(gr)
    # print(calculate_part_one(gr))  # 1344578
    print(calculate_part_two(gr))  # 814302


if __name__ == "__main__":
    test()
