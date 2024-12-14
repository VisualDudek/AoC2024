from collections import defaultdict
import re
from typing import Tuple


test_data = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def parse_data(s: str):
    """ """
    pattern = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )

    matches = pattern.findall(s)

    # Parse results
    parsed_data = {}
    for id, match in enumerate(matches):
        parsed_data[id] = {
            "A": (int(match[0]), int(match[1])),
            "B": (int(match[2]), int(match[3])),
            "Prize": (int(match[4]), int(match[5])),
        }
    return parsed_data


def parse_data_two(s: str):
    """ """
    pattern = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )

    matches = pattern.findall(s)

    # Parse results
    parsed_data = {}
    for id, match in enumerate(matches):
        parsed_data[id] = {
            "A": (int(match[0]), int(match[1])),
            "B": (int(match[2]), int(match[3])),
            "Prize": (int(match[4]) + 10000000000000, int(match[5]) + 10000000000000),
        }
    return parsed_data


def pay_to_win(a: Tuple[int, int], b: Tuple[int, int], p: Tuple[int, int]) -> int:
    """
    Calculate the cost to win the prize.
    """
    res = set()
    for i in range(101):
        for j in range(101):
            if a[0] * i + b[0] * j == p[0] and a[1] * i + b[1] * j == p[1]:
                res.add((i, j))
    print(res)
    if len(res) > 0:
        return min([x * 3 + y * 1 for x, y in res])
    return 0


def pay_to_win_two(a: Tuple[int, int], b: Tuple[int, int], p: Tuple[int, int]) -> int:
    """
    Calculate the cost to win the prize.
    """
    res = set()
    for i in range(max(p[0] // a[0], p[1] // a[1]) + 1):
        for j in range(max((p[0] - a[0] * i) // b[0], (p[1] - a[1] * i) // b[1]) + 1):
            if a[0] * i + b[0] * j == p[0] and a[1] * i + b[1] * j == p[1]:
                res.add((i, j))
    print(res)
    if len(res) > 0:
        return min([x * 3 + y * 1 for x, y in res])
    return 0


def part1(s: str) -> int:
    d = parse_data(s)
    res = 0
    for _ in d.values():
        res += pay_to_win(_["A"], _["B"], _["Prize"])
    return res


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def test():
    d = parse_data_two(test_data)
    print(d)
    pay_to_win_two(d[0]["A"], d[0]["B"], d[0]["Prize"])


if __name__ == "__main__":
    # test()
    # print(f"Testing Part 1: {part1(test_data)}")
    print(f"Testing Part 1: {part1(get_file_data('./data/013.txt'))}")  # 31065
