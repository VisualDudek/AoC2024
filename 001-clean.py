from collections import Counter
from typing import List

test_data = """3   4
4   3
2   5
1   3
3   9
3   3"""


def parse(data: str) -> tuple[list[int], list[int]]:
    """
    Parse the data into two lists of integers.
    """
    left: List[int] = []
    right: List[int] = []
    for line in data.split("\n"):
        left_col, right_col = line.split()
        left.append(int(left_col))
        right.append(int(right_col))

    return left, right


def total_distance(left: List[int], right: List[int]) -> int:
    """
    Calculate the total distance between the two lists.
    """
    left.sort()
    right.sort()

    return sum([abs(x - y) for x, y in zip(left, right)])


def similarity_score(left: List[int], right: List[int]) -> int:
    """
    Calculate the similarity score between the two lists.
    no need to sort lists but I need to turn second list into Counter dict?
    """
    c = Counter(right)

    return sum([item * c[item] for item in left])


def part1(data: str) -> int:
    left, right = parse(data)
    return total_distance(left, right)


def part2(data: str) -> int:
    left, right = parse(data)
    return similarity_score(left, right)


if __name__ == "__main__":
    print(f"Testing Part 1: {part1(test_data)}")  # 11
    print(f"Testing Part 1: {part2(test_data)}")  # 31

    with open("./data/001.txt", "r") as f:
        data = f.read()

    assert part1(data) == 1722302
    assert part2(data) == 20373490
