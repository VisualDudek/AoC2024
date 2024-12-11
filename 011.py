from typing import List


test_data = """125 17"""


def parse_data(data: str) -> List[int]:
    """
    Parse the data into a list of integers.
    """
    return [int(x) for x in data.split()]


def rule_one(x: int) -> List[int] | bool:

    if x == 0:
        return [1]
    return False


from functools import lru_cache


@lru_cache(maxsize=None)
def rule_two(x: int) -> List[int] | bool:
    """
    Rule 2: If nuber havse ans even number of digits
    """
    if len(str(x)) % 2 == 0:
        left, right = str(x)[: len(str(x)) // 2], str(x)[len(str(x)) // 2 :]
        return [int(left), int(right)]
    return False


def blink(data: List[int]) -> List[int]:
    """
    Blink the data.
    """
    new_data: List[int] = []
    for x in data:
        # if rule_one(x):
        # new_data.extend(rule_one(x))
        if x == 0:
            new_data.append(1)
        elif rule_two(x):
            new_data.extend(rule_two(x))
        else:
            new_data.append(x * 2024)
    return new_data


@lru_cache(maxsize=None)
def blinkrecursive(depth: int, number: int):
    """
    Recursive blink.
    """
    if depth == 0:
        # print(number)
        return 1
    if number == 0:
        # MEGA BUG brakowało returna, debugowałem to ok 1h ...
        # blinkrecursive(depth - 1, 1)
        return blinkrecursive(depth - 1, 1)
    elif rule_two(number):
        left, right = rule_two(number)
        return blinkrecursive(depth - 1, left) + blinkrecursive(depth - 1, right)

    return blinkrecursive(depth - 1, number * 2024)


def test_rec():
    data = parse_data("125 17")

    res = 0
    for _ in data:
        res += blinkrecursive(25, _)

    print(f"res: {res}")


def part2(s: str) -> None:
    data = parse_data(s)
    res = 0
    for _ in data:
        res += blinkrecursive(75, _)
    print(f"res: {res}")
    pass


def test():
    data = parse_data(test_data)

    for _ in range(5):
        data = blink(data)
        print(data)


def part1(s: str) -> int:
    data = parse_data(s)
    for _ in range(25):
        data = blink(data)
    return len(data)


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


if __name__ == "__main__":
    # test_rec()

    file_data = get_file_data("./data/011.txt")

    # print(part1(file_data))  # 220722
    # print(part2(file_data))  #

    part2(file_data)
