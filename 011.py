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
        if rule_one(x):
            new_data.extend(rule_one(x))
        elif rule_two(x):
            new_data.extend(rule_two(x))
        else:
            new_data.append(x * 2024)
    return new_data


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
    # test()

    file_data = get_file_data("./data/011.txt")

    print(part1(file_data))  # 220722
