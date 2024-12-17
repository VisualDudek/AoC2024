from collections import defaultdict, deque
from typing import TypeAlias

test_data = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<"""

Grid: TypeAlias = defaultdict[complex, str]
Position: TypeAlias = complex
OFFSETS: dict[str, complex] = {
    "^": -1j,
    "v": 1j,
    "<": -1,
    ">": 1,
}


def parse_data(s: str) -> tuple[Grid, complex, str]:
    grid: Grid = defaultdict(
        lambda: "#"
    )  # this default_factory had no use case in this problem BC you are not going to look up values that are not in the grid
    line_iter = iter(s.split("\n"))
    robot: complex | None = None
    for y, line in enumerate(line_iter):
        # emply line means end of grid
        if not line:
            break
        for x, char in enumerate(line):
            grid[x + y * 1j] = char
            if char == "@":
                robot = x + y * 1j

    assert robot is not None
    moves: str = "".join(line_iter)

    return grid, robot, moves


def part1(grid: Grid, robot: Position, moves: str):
    """
    Execute the moves
    DO NOT LIKE LOGIC IN THIS FUNCTION, THERE IS SO MANY IMPLICTE THINGS GOING ON
    """
    # Execute the moves
    for move in moves:
        # Get the new position
        new_position: Position = robot + OFFSETS[move]
        # 3 branches
        # (1) can move "." default move
        # (2) wall "#" continue next move
        # (3) box "O"

        if grid[new_position] == "#":
            continue
        elif grid[new_position] == "O":
            box = new_position
            while (tile := grid[box]) == "O":
                box += OFFSETS[move]
            if tile == "#":
                continue
            # implicite grid[new_position] == "."
            # TRICK: teleport box
            grid[box], grid[new_position] = "O", "."

        # move robot
        grid[robot], grid[new_position] = grid[new_position], grid[robot]
        robot = new_position

    pass


Stack: TypeAlias = deque[Position]


def part_with_deque(grid: Grid, robot: Position, moves: str) -> int:
    """
    Execute the moves
    IMPLEMENT A STACK TO KEEP TRACK ADJACENT BOXES to get rid of swap trick
    """
    # Execute the moves
    for move in moves:
        # Get the new position
        new_position: Position = robot + OFFSETS[move]

        if grid[new_position] == "#":
            continue
        elif grid[new_position] == "O":
            box = new_position
            stack_of_boxes: Stack = deque()
            while (tile := grid[box]) == "O":
                stack_of_boxes.append(box)
                box += OFFSETS[move]
            if tile == "#":
                continue
            # implicite grid[new_position] == "."
            # TRICK: teleport box
            # grid[box], grid[new_position] = "O", "."
            # move boxes
            while stack_of_boxes:
                box = stack_of_boxes.pop()
                grid[box], grid[box + OFFSETS[move]] = (
                    grid[box + OFFSETS[move]],
                    grid[box],
                )

        # move robot implicite: can move or box are already moved
        grid[robot], grid[new_position] = grid[new_position], grid[robot]
        robot = new_position

    return int(sum(p.real + 100 * p.imag for p, value in grid.items() if value == "O"))


def print_grid(grid: Grid):
    """
    Print the grid.
    """

    # Get max x and y values
    x_max = int(max(pos.real for pos in grid))
    y_max = int(max(pos.imag for pos in grid))

    # Print the grid
    for y in range(y_max + 1):
        for x in range(x_max + 1):
            print(grid[x + y * 1j], end="")
        print()


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def test():
    grid, robot, moves = parse_data(test_data)
    grid, robot, moves = parse_data(get_file_data("./data/015.txt"))
    # print(grid)
    print_grid(grid)
    print(robot)
    print(moves)
    res = part_with_deque(grid, robot, moves)
    print(res)


if __name__ == "__main__":
    test()
