from collections import defaultdict
from typing import NamedTuple, Tuple, TypeAlias, List


test_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

large_data = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^"""

small_data = """#######
#...#.#
#.....#
#..OO@#
#..O..#
#.....#
#######

<vv<<^^<<^^"""

edge_data = """######
#....#
#..#.#
#....#
#.O..#
#.OO@#
#.O..#
#....#
######

<vv<<^^^"""

Map: TypeAlias = defaultdict[Tuple[int, int], str]


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


def parse_data_two(s: str):
    map: Map = defaultdict(str)
    lines = s.split("\n")
    path: List[str] = []
    for y, line in enumerate(lines):
        if line.startswith("#"):
            for x, char in enumerate(line):
                if char == "#":
                    map[(x * 2, y)] = "#"
                    map[(x * 2 + 1, y)] = "#"
                elif char == "O":
                    map[(x * 2, y)] = "["
                    map[(x * 2 + 1, y)] = "]"
                elif char == ".":
                    map[(x * 2, y)] = "."
                    map[(x * 2 + 1, y)] = "."
                elif char == "@":
                    map[(x * 2, y)] = "@"
                    map[(x * 2 + 1, y)] = "."
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
        elif map[new_postion] in ["[", "]"]:
            box: Box = get_box(Point(new_postion[0], new_postion[1]), map)
            if moving_box(map, box, map_direction(direction)):
                map[postion] = "."
                map[new_postion] = "@"
                postion = new_postion
        # print(direction)
        # show_map(map)
        # print()


class Point(NamedTuple):
    x: int
    y: int


class Box(NamedTuple):
    left: Point
    right: Point


def get_box(p: Point, map: Map) -> Box:
    if map[p.x, p.y] == "[":  # box is on the left
        return Box(left=p, right=Point(p.x + 1, p.y))
    return Box(left=Point(p.x - 1, p.y), right=p)


def moving_box(map: Map, box: Box, move: Tuple[int, int]) -> bool:
    # easy part is moving the box to the left or right
    if move == (1, 0):  # can move to the right?
        if map[box.right.x + 1, box.right.y] == "[":
            next_box: Box = get_box(Point(box.right.x + 1, box.right.y), map)
            if moving_box(map, next_box, move):
                # move the box to the right
                map[box.right.x + 1, box.right.y] = "]"
                map[box.left.x + 1, box.left.y] = "["
                map[box.left.x, box.left.y] = "."
                return True
        elif map[box.right.x + 1, box.right.y] == ".":
            map[box.right.x + 1, box.right.y] = "]"
            map[box.left.x + 1, box.left.y] = "["
            map[box.left.x, box.left.y] = "."
            return True
        return False  # otherwise, can't move the box to the right
    elif move == (-1, 0):  # can move to the left?
        if map[box.left.x - 1, box.left.y] == "]":
            next_box: Box = get_box(Point(box.left.x - 1, box.left.y), map)
            if moving_box(map, next_box, move):
                # move the box to the left
                map[box.left.x - 1, box.left.y] = "["
                map[box.right.x - 1, box.right.y] = "]"
                map[box.right.x, box.right.y] = "."
                return True
        elif map[box.left.x - 1, box.left.y] == ".":
            map[box.left.x - 1, box.left.y] = "["
            map[box.right.x - 1, box.right.y] = "]"
            map[box.right.x, box.right.y] = "."
            return True
        return False
    # hard part is moving the box up or down
    elif move == (0, -1):  # can move up ?
        if (
            map[box.left.x, box.left.y - 1] == "["
            and map[box.right.x, box.right.y - 1] == "]"
        ):
            next_box: Box = Box(
                left=Point(box.left.x, box.left.y - 1),
                right=Point(box.right.x, box.right.y - 1),
            )
            if moving_box(map, next_box, move):
                # move the box up
                map[box.left.x, box.left.y - 1] = "["
                map[box.right.x, box.right.y - 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "."
            and map[box.right.x, box.right.y - 1] == "."
        ):
            # move the box up
            map[box.left.x, box.left.y - 1] = "["
            map[box.right.x, box.right.y - 1] = "]"
            map[box.left.x, box.left.y] = "."
            map[box.right.x, box.right.y] = "."
            return True
        elif (
            map[box.left.x, box.left.y - 1] == "]"
            and map[box.right.x, box.right.y - 1] == "."
        ):
            next_box: Box = get_box(Point(box.left.x, box.left.y - 1), map)
            if moving_box(map, next_box, move):
                # move the box up
                map[box.left.x, box.left.y - 1] = "["
                map[box.right.x, box.right.y - 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "."
            and map[box.right.x, box.right.y - 1] == "["
        ):
            next_box: Box = get_box(Point(box.right.x, box.right.y - 1), map)
            if moving_box(map, next_box, move):
                # move the box up
                map[box.left.x, box.left.y - 1] = "["
                map[box.right.x, box.right.y - 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "]"
            and map[box.right.x, box.right.y - 1] == "["
        ):
            next_box_left: Box = get_box(Point(box.left.x, box.left.y - 1), map)
            next_box_right: Box = get_box(Point(box.right.x, box.right.y - 1), map)
            if can_moving_box(map, next_box_left, move) and can_moving_box(
                map, next_box_right, move
            ):
                moving_box(map, next_box_left, move)
                moving_box(map, next_box_right, move)
                # move the box up
                map[box.left.x, box.left.y - 1] = "["
                map[box.right.x, box.right.y - 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        return False
    elif move == (0, 1):  # can move down ?
        if (
            map[box.left.x, box.left.y + 1] == "["
            and map[box.right.x, box.right.y + 1] == "]"
        ):
            next_box: Box = Box(
                left=Point(box.left.x, box.left.y + 1),
                right=Point(box.right.x, box.right.y + 1),
            )
            if moving_box(map, next_box, move):
                # move the box down
                map[box.left.x, box.left.y + 1] = "["
                map[box.right.x, box.right.y + 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "."
            and map[box.right.x, box.right.y + 1] == "."
        ):
            # move the box down
            map[box.left.x, box.left.y + 1] = "["
            map[box.right.x, box.right.y + 1] = "]"
            map[box.left.x, box.left.y] = "."
            map[box.right.x, box.right.y] = "."
            return True
        elif (
            map[box.left.x, box.left.y + 1] == "]"
            and map[box.right.x, box.right.y + 1] == "."
        ):
            next_box: Box = get_box(Point(box.left.x, box.left.y + 1), map)
            if moving_box(map, next_box, move):
                # move the box down
                map[box.left.x, box.left.y + 1] = "["
                map[box.right.x, box.right.y + 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "."
            and map[box.right.x, box.right.y + 1] == "["
        ):
            next_box: Box = get_box(Point(box.right.x, box.right.y + 1), map)
            if moving_box(map, next_box, move):
                # move the box down
                map[box.left.x, box.left.y + 1] = "["
                map[box.right.x, box.right.y + 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "]"
            and map[box.right.x, box.right.y + 1] == "["
        ):
            next_box_left: Box = get_box(Point(box.left.x, box.left.y + 1), map)
            next_box_right: Box = get_box(Point(box.right.x, box.right.y + 1), map)
            if can_moving_box(map, next_box_left, move) and can_moving_box(
                map, next_box_right, move
            ):
                moving_box(map, next_box_left, move)
                moving_box(map, next_box_right, move)
                # move the box down
                map[box.left.x, box.left.y + 1] = "["
                map[box.right.x, box.right.y + 1] = "]"
                map[box.left.x, box.left.y] = "."
                map[box.right.x, box.right.y] = "."
                return True
        return False

    return False


def can_moving_box(map: Map, box: Box, move: Tuple[int, int]) -> bool:
    # hard part is moving the box up or down
    if move == (0, -1):  # can move up ?
        if (
            map[box.left.x, box.left.y - 1] == "["
            and map[box.right.x, box.right.y - 1] == "]"
        ):
            next_box: Box = Box(
                left=Point(box.left.x, box.left.y - 1),
                right=Point(box.right.x, box.right.y - 1),
            )
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "."
            and map[box.right.x, box.right.y - 1] == "."
        ):
            return True
        elif (
            map[box.left.x, box.left.y - 1] == "]"
            and map[box.right.x, box.right.y - 1] == "."
        ):
            next_box: Box = get_box(Point(box.left.x, box.left.y - 1), map)
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "."
            and map[box.right.x, box.right.y - 1] == "["
        ):
            next_box: Box = get_box(Point(box.right.x, box.right.y - 1), map)
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y - 1] == "]"
            and map[box.right.x, box.right.y - 1] == "["
        ):
            next_box_left: Box = get_box(Point(box.left.x, box.left.y - 1), map)
            next_box_right: Box = get_box(Point(box.right.x, box.right.y - 1), map)
            if can_moving_box(map, next_box_left, move) and can_moving_box(
                map, next_box_right, move
            ):
                return True
        return False
    elif move == (0, 1):  # can move down ?
        if (
            map[box.left.x, box.left.y + 1] == "["
            and map[box.right.x, box.right.y + 1] == "]"
        ):
            next_box: Box = Box(
                left=Point(box.left.x, box.left.y + 1),
                right=Point(box.right.x, box.right.y + 1),
            )
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "."
            and map[box.right.x, box.right.y + 1] == "."
        ):
            return True
        elif (
            map[box.left.x, box.left.y + 1] == "]"
            and map[box.right.x, box.right.y + 1] == "."
        ):
            next_box: Box = get_box(Point(box.left.x, box.left.y + 1), map)
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "."
            and map[box.right.x, box.right.y + 1] == "["
        ):
            next_box: Box = get_box(Point(box.right.x, box.right.y + 1), map)
            if can_moving_box(map, next_box, move):
                return True
        elif (
            map[box.left.x, box.left.y + 1] == "]"
            and map[box.right.x, box.right.y + 1] == "["
        ):
            next_box_left: Box = get_box(Point(box.left.x, box.left.y + 1), map)
            next_box_right: Box = get_box(Point(box.right.x, box.right.y + 1), map)
            if can_moving_box(map, next_box_left, move) and can_moving_box(
                map, next_box_right, move
            ):
                return True
        return False

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
        if value == "[":
            solution += x + 100 * y
    return solution


def calculate_solution_two(map: Map) -> int:
    # find max x and y
    max_x = 0
    max_y = 0
    for x, y in map.keys():
        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y

    solution = 0
    for (x, y), value in map.items():
        if value == "[":
            xs = min(x, max_x - x - 1)
            ys = min(y, max_y - y)

            solution += xs + 100 * ys
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


def test_two():
    # map, path = parse_data_two(small_data)
    map, path = parse_data_two(large_data)
    show_map(map)
    follow_path(map, path, find_starting_position(map))
    print(calculate_solution_one(map))


def part2(data: str) -> int:
    # map, path = parse_data_two(small_data)
    map, path = parse_data_two(data)
    follow_path(map, path, find_starting_position(map))
    show_map(map)
    return calculate_solution_one(map)


if __name__ == "__main__":
    # test()
    file_data = get_file_data("./data/015.txt")
    # print(f"Part 1: {part1(file_data)}")  # 1538871
    print(f"Part 2: {part2(file_data)}")  # 1543338

    # test_two()
