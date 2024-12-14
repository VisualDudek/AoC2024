import re
from typing import Iterator, NamedTuple, TypeAlias, cast


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


class Button(NamedTuple):
    x: int
    y: int


class Prize(NamedTuple):
    x: int
    y: int


Game: TypeAlias = tuple[Button, Button, Prize]


def parse_data(s: str) -> Iterator[Game]:

    pattern = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )

    matches = pattern.findall(s)

    # Parse results
    for match in matches:
        A = Button(int(match[0]), int(match[1]))
        B = Button(int(match[2]), int(match[3]))
        P = Prize(int(match[4]), int(match[5]))

        yield cast(Game, tuple([A, B, P]))


def parse_data_two(s: str) -> Iterator[Game]:

    pattern = re.compile(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)"
    )

    matches = pattern.findall(s)
    N = 10000000000000

    # Parse results
    for match in matches:
        A = Button(int(match[0]), int(match[1]))
        B = Button(int(match[2]), int(match[3]))
        P = Prize(int(match[4]) + N, int(match[5]) + N)

        yield cast(Game, tuple([A, B, P]))


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def solve_game(game: Game) -> int:
    A, B, P = game

    det = A.x * B.y - A.y * B.x
    det_x = P.x * B.y - P.y * B.x
    det_y = A.x * P.y - A.y * P.x

    a = det_x // det
    b = det_y // det

    if det_x % det == 0 and det_y % det == 0:
        return a * 3 + b

    return 0


def test():
    it = parse_data(test_data)
    solution = sum([solve_game(game) for game in it])
    print(solution)


def part1():
    file_data = get_file_data("./data/013.txt")
    it = parse_data(file_data)
    solution = sum([solve_game(game) for game in it])
    print(solution)


def part2():
    file_data = get_file_data("./data/013.txt")
    it = parse_data_two(file_data)
    solution = sum([solve_game(game) for game in it])
    print(solution)


if __name__ == "__main__":
    # test()
    # part1()
    part2()
