from collections import defaultdict
from typing import Tuple, TypeAlias, List


test_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

Map: TypeAlias = defaultdict[Tuple[int, int], str]

MAX_X: int = 0
MAX_Y: int = 0


def parse_data(s: str):
    map: Map = defaultdict(str)
    lines = s.split("\n")
    path: List[str] = []
    for y, line in enumerate(lines):
        if line.startswith("#"):
            for x, char in enumerate(line):
                map[(x, y)] = char
        elif line:
            path.extend(list(line))

    return map, path


def find_starting_position(map: Map) -> Tuple[int, int]:
    for (x, y), value in map.items():
        if value == "@":
            return (x, y)
    return (0, 0)


def map_direction(direction: str) -> Tuple[int, int]:
    if direction == "^":
        return (0, -1)
    if direction == "v":
        return (0, 1)
    if direction == "<":
        return (-1, 0)
    if direction == ">":
        return (1, 0)
    return (0, 0)


def follow_path(map: Map, path: List[str], start_position: Tuple[int, int]):
    postion = start_position
    for direction in path:
        new_postion = (
            postion[0] + map_direction(direction)[0],
            postion[1] + map_direction(direction)[1],
        )
        if map[new_postion] == "#":
            continue
        elif map[new_postion] == ".":
            map[postion] = "."
            map[new_postion] = "@"
            postion = new_postion
        elif map[new_postion] == "O":
            if moving_boxes(map, new_postion, map_direction(direction)):
                map[postion] = "."
                map[new_postion] = "@"
                postion = new_postion
        # print(direction)
        # show_map(map)


def moving_boxes(map: Map, position: Tuple[int, int], move: Tuple[int, int]) -> bool:
    new_position = (position[0] + move[0], position[1] + move[1])
    if map[new_position] == "O":
        if moving_boxes(map, new_position, move):
            map[new_position] = "O"
            map[position] = "."
            return True
    elif map[new_position] == ".":
        map[new_position] = "O"
        map[position] = "."
        return True
    return False


def show_map(map: Map):
    # find max x and y
    max_x = 0
    max_y = 0
    for x, y in map.keys():
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print(map[(x, y)], end="")
        print()


def calculate_solution_one(map: Map) -> int:
    solution = 0
    for (x, y), value in map.items():
        if value == "O":
            solution += x + 100 * y
    return solution


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def test():
    map, path = parse_data(test_data)
    print(map)
    print(path)
    print(find_starting_position(map))
    show_map(map)
    follow_path(map, path, find_starting_position(map))
    print(calculate_solution_one(map))


def part1(data: str) -> int:
    map, path = parse_data(data)
    follow_path(map, path, find_starting_position(map))
    return calculate_solution_one(map)


if __name__ == "__main__":
    # test()
    file_data = get_file_data("./data/015.txt")
    print(f"Part 1: {part1(file_data)}")  # 1538871
