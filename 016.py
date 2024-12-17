from collections import deque
from enum import StrEnum
from typing import List, TypeAlias, cast
from dataclasses import dataclass


test_data = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

test_data_002 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################"""


class Tile(StrEnum):
    WALL = "#"
    EMPTY = "."
    START = "S"
    END = "E"


Pos: TypeAlias = complex
Grid: TypeAlias = dict[Pos, Tile]


@dataclass
class Map:
    grid: Grid
    start: Pos = None  # type: ignore
    end: Pos = None  # type: ignore

    def __post_init__(self):
        self.start = self.find_start()
        self.end = self.find_end()

    def find_start(self) -> Pos:
        for pos, tile in self.grid.items():
            if tile == Tile.START:
                return pos
        raise ValueError("Start not found")

    def find_end(self) -> Pos:
        for pos, tile in self.grid.items():
            if tile == Tile.END:
                return pos
        raise ValueError("End not found")

    def show(self):
        max_x = int(max(self.grid, key=lambda x: x.real).real)
        max_y = int(max(self.grid, key=lambda x: x.imag).imag)

        for y in range(max_y + 1):
            for x in range(max_x + 1):
                print(self.grid.get(x + y * 1j, " "), end="")
            print()

    def show_postion(self, postion: Pos):
        """
        Print the grid with the current position.
        """
        # Get max x and y values
        x_max = int(max(pos.real for pos in self.grid))
        y_max = int(max(pos.imag for pos in self.grid))

        # Print the grid
        for y in range(y_max + 1):
            for x in range(x_max + 1):
                if x + y * 1j == postion:
                    print("@", end="")
                else:
                    print(self.grid.get(x + y * 1j, " "), end="")
            print()


def parse_data(s: str) -> Grid:
    grid: Grid = {}
    lines = s.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            assert char in Tile, f"Invalid character {char}"
            grid[x + y * 1j] = cast(Tile, char)

    return grid


@dataclass
class Node:
    pos: complex
    direction: Pos
    value: int = 0


def traverse(grid: Map):
    direction = 1 + 0j  # start facing east
    node = Node(grid.start, direction)
    next_stack = deque([node])
    visited: List[complex] = []

    while next_stack:
        node = next_stack.popleft()
        visited.append(node.pos)
        # grid.show_postion(node.pos)
        if node.pos == grid.end:
            print(node.value)
            break

        # find moveable positions and add them into next_stack
        for rotate in [1 + 0j, 1j, -1j]:
            new_pos = node.pos + node.direction * rotate
            if new_pos in visited:
                continue
            if grid.grid[new_pos] in (Tile.EMPTY, Tile.END):
                if rotate == 1:
                    next_stack.appendleft(Node(new_pos, node.direction, node.value + 1))
                else:
                    next_stack.append(
                        Node(
                            new_pos, node.direction * rotate, node.value + 1_001
                        )  # 1_000 for turning and 1 for moving
                    )

    pass


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    # grid_data = parse_data(test_data_002)
    grid_data = parse_data(get_file_data("./data/016.txt"))  # 122492
    grid = Map(grid_data)
    # grid.show()
    traverse(grid)
