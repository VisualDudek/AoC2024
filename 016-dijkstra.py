from collections import deque
from enum import StrEnum
import heapq
from typing import Iterator, List, Tuple, TypeAlias, cast
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

    def show_positions(self, positions: List[complex]):
        """
        Print the grid with the current position.
        """
        # Get max x and y values
        x_max = int(max(pos.real for pos in self.grid))
        y_max = int(max(pos.imag for pos in self.grid))

        # Print the grid
        for y in range(y_max + 1):
            for x in range(x_max + 1):
                if x + y * 1j in positions:
                    print("O", end="")
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

    def __lt__(self, other: "Node") -> bool:
        return self.value < other.value


def traverse(grid: Map):
    direction = 1 + 0j  # start facing east
    node = Node(grid.start, direction)
    # init distance with infinity, except start node
    distance = {pos: float("inf") for pos in grid.grid if grid.grid[pos] != Tile.WALL}
    distance[grid.start] = 0

    # min-heap to store (distance, node)
    min_heap: List[Tuple[float, Node]] = [(0, node)]

    # track visited nodes
    visited = set()

    # predessor map for path reconstruction
    pred: dict[complex, complex] = {}

    while min_heap:
        # pop the node with the smallest distance
        current_distance, node = heapq.heappop(min_heap)

        # skip if this node has been visited
        if node.pos in visited:
            continue
        visited.add(node.pos)

        if node.pos == grid.end:
            print(distance[node.pos])
            break

        # explore neighbors
        # return a iterator of neighbors for given node with cost
        for neighbor in get_neighbours(node, grid):

            grid.show_postion(neighbor.pos)
            pass
            # if a shorter path to neighbor is found, update it
            if neighbor.value < distance[neighbor.pos]:
                distance[neighbor.pos] = neighbor.value
                pred[neighbor.pos] = node.pos
                heapq.heappush(min_heap, (neighbor.value, neighbor))

    return pred


def get_neighbours(node: Node, grid: Map) -> Iterator[Node]:
    for rotate in [1 + 0j, 1j, -1j]:
        new_pos = node.pos + node.direction * rotate
        if grid.grid[new_pos] in (Tile.EMPTY, Tile.END):
            if rotate == 1:
                yield Node(new_pos, node.direction, node.value + 1)
            else:
                yield Node(new_pos, node.direction * rotate, node.value + 1_001)


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def reconstruct_path(
    pred: dict[complex, complex], start: complex, end: complex
) -> List[complex]:
    path = []
    node = end
    while node != start:
        path.append(node)
        node = pred[node]
    path.append(start)
    return path[::-1]


if __name__ == "__main__":
    grid_data = parse_data(test_data)  # 7036
    # grid_data = parse_data(test_data_002)  # 11048
    # grid_data = parse_data(get_file_data("./data/016.txt"))  # 122492
    grid = Map(grid_data)
    # grid.show()
    pred = traverse(grid)
    path = reconstruct_path(pred, grid.start, grid.end)
    grid.show_positions(path)
