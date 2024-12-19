from collections import defaultdict
from dataclasses import dataclass
import itertools
import re
from typing import Dict, NamedTuple, Tuple, TypeAlias

test_data_001 = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3"""

test_data_002 = """p=2,4 v=2,-3"""


class Pos(NamedTuple):
    x: int
    y: int


class Vel(NamedTuple):
    x: int
    y: int


Robots: TypeAlias = Dict[int, Tuple[Pos, Vel]]


@dataclass
class Grid:
    max_x: int
    max_y: int

    def show(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                # print("#" if (x, y) in self else ".", end="")
                print(".", end="")
            print()

    def show_robots(self, robots: Robots):

        position_counter = defaultdict(lambda: 0)
        for _, (pos, _) in robots.items():
            position_counter[pos] += 1

        for y in range(self.max_y):
            for x in range(self.max_x):
                if (no := position_counter[Pos(x, y)]) > 0:
                    print(no, end="")
                else:
                    print(".", end="")
            print()
        print()

    def show_robots_unique(self, robots: Robots):

        position_counter = defaultdict(lambda: 0)
        for _, (pos, _) in robots.items():
            position_counter[pos] += 1

        if not any(item > 1 for item in position_counter.values()):
            for y in range(self.max_y):
                for x in range(self.max_x):
                    if (no := position_counter[Pos(x, y)]) > 0:
                        print(no, end="")
                    else:
                        print(".", end="")
                print()
            print()


def parse_data(s: str) -> Robots:

    pattern = r"-?\d+"

    robots: Robots = {}

    lines = s.split("\n")
    for id, line in enumerate(lines):
        numbers = re.findall(pattern, line)
        pos = Pos(int(numbers[0]), int(numbers[1]))
        vel = Vel(int(numbers[2]), int(numbers[3]))
        robots[id] = (pos, vel)

    return robots


def part1(robots: Robots, grid: Grid) -> Robots:

    grid.show_robots(robots)

    for step in range(10000):
        print(f"After step {step+1}")
        for id, (pos, vel) in robots.items():
            robots[id] = (
                Pos((pos.x + vel.x) % grid.max_x, (pos.y + vel.y) % grid.max_y),
                vel,
            )

        grid.show_robots_unique(robots)

    return robots


def calculate_solution_one(robots: Robots, grid: Grid) -> int:
    if grid.max_x % 2 == 0:
        x1 = grid.max_x // 2
        x2 = x1
    else:
        x1 = grid.max_x // 2
        x2 = x1 + 1

    if grid.max_y % 2 == 0:
        y1 = grid.max_y // 2
        y2 = y1
    else:
        y1 = grid.max_y // 2
        y2 = y1 + 1

    position_counter = defaultdict(lambda: 0)
    for _, (pos, _) in robots.items():
        position_counter[pos] += 1

    # top left
    top_left = 0
    for y in range(y1):
        for x in range(x1):
            top_left += position_counter[Pos(x, y)]

    # top right
    top_right = 0
    for y in range(y1):
        for x in range(x2, grid.max_x):
            top_right += position_counter[Pos(x, y)]

    # bottom left
    bottom_left = 0
    for y in range(y2, grid.max_y):
        for x in range(x1):
            bottom_left += position_counter[Pos(x, y)]

    # bottom right
    bottom_right = 0
    for y in range(y2, grid.max_y):
        for x in range(x2, grid.max_x):
            bottom_right += position_counter[Pos(x, y)]

    return top_left * top_right * bottom_left * bottom_right


def calculate_density(robots: Robots, grid: Grid) -> float:

    lst_points = [pos for pos, _ in robots.values()]

    permutations = itertools.permutations(lst_points, 2)

    sum_distance = sum(euclidean_distance(pos1, pos2) for pos1, pos2 in permutations)

    return sum_distance


def part2(robots: Robots, grid: Grid) -> Robots:

    grid.show_robots(robots)

    min = float("inf")

    for step in range(10000):
        print(f"After step {step+1}")
        for id, (pos, vel) in robots.items():
            robots[id] = (
                Pos((pos.x + vel.x) % grid.max_x, (pos.y + vel.y) % grid.max_y),
                vel,
            )

        if (density := calculate_density(robots, grid)) < min:
            min = density
        pass

        if density <= 7845275:
            grid.show_robots(robots)
            print(min)
            input("Press Enter to continue...")
        # print(f"Min Density: {min:,.2f}")

    print(f"Min density: {min}")

    return robots


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def euclidean_distance(p1: Pos, p2: Pos) -> float:
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2) ** 0.5


def test():
    # data = parse_data(test_data_001) # 12
    # grid = Grid(11, 7)
    data = parse_data(get_file_data("./data/014.txt"))  # 229980828
    grid = Grid(101, 103)
    part1(data, grid)
    # print(calculate_solution_one(data, grid))

    # part2(data, grid)


if __name__ == "__main__":
    test()
