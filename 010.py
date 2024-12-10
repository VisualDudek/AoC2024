from collections import defaultdict

test_data_01 = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732"""


def parse_data(s: str) -> dict[tuple[int, int], int]:
    """
    Parse the data into a dictionary of (x, y) -> value.
    """
    data: dict[tuple[int, int], int] = {}
    for y, line in enumerate(s.split("\n")):
        for x, value in enumerate(line):
            data[(x, y)] = int(value)
    return data


def reverse_dict(
    d: dict[tuple[int, int], int]
) -> defaultdict[int, list[tuple[int, int]]]:
    """
    Reverse the dictionary.
    """
    reversed_dict: defaultdict[int, list[tuple[int, int]]] = defaultdict(list)
    for (x, y), value in d.items():
        reversed_dict[value].append((x, y))
    return reversed_dict


def get_hiking_trails_for_position(
    d: dict[tuple[int, int], int], position: tuple[int, int]
) -> dict[tuple[int, int], int]:
    """
    Get the hiking trails for a given position.
    """
    hiking_trails: dict[tuple[int, int], int] = {}
    hiking_trails[position] = 0
    traverse(d, position, hiking_trails)
    return hiking_trails


def count_9a(d: dict[tuple[int, int], int]) -> int:
    """
    Count the number of 9s in the dictionary.
    """
    return sum(1 for value in d.values() if value == 9)


def traverse(
    d: dict[tuple[int, int], int],
    position: tuple[int, int],
    hiking_trails: dict[tuple[int, int], int],
):
    real, imag = position
    complex_position = complex(real, imag)
    # for left, right, up, down update hiking_trails
    for direction in [1, -1j, -1, 1j]:
        new_position: complex = complex_position + direction
        x, y = int(new_position.real), int(new_position.imag)
        if adj_position_value := d.get((x, y), False):
            if d[(x, y)] - d[position] == 1:
                hiking_trails[(x, y)] = adj_position_value
                traverse(d, (x, y), hiking_trails)


def get_all_possible_hikes(
    d: dict[tuple[int, int], int], position: tuple[int, int]
) -> int:
    res = [0]
    traverse_all_possible_hikes(d, position, res)
    return res[0]


def traverse_all_possible_hikes(
    d: dict[tuple[int, int], int],
    position: tuple[int, int],
    count: list[int],
):
    real, imag = position
    complex_position = complex(real, imag)
    # for left, right, up, down update hiking_trails
    for direction in [1, -1j, -1, 1j]:
        new_position: complex = complex_position + direction
        x, y = int(new_position.real), int(new_position.imag)
        if d.get((x, y), False):
            if d[(x, y)] - d[position] == 1 and d[(x, y)] == 9:
                count[0] += 1
            elif d[(x, y)] - d[position] == 1:
                traverse_all_possible_hikes(d, (x, y), count)


def show_map(map: dict[tuple[int, int], int], size: int):
    lst = []
    # fill array of size x size with .
    for _ in range(size):
        lst.append(["." for _ in range(size)])

    # for each key in map, update lst with value
    for (x, y), value in map.items():
        lst[y][x] = str(value)

    # print each row in lst
    for row in lst:
        print(" ".join(row))


def part1(data: str) -> int:
    d = parse_data(data)
    res = 0
    for item in reverse_dict(d)[0]:
        res += count_9a(get_hiking_trails_for_position(d, item))
    return res


def part2(data: str) -> int:
    d = parse_data(data)
    res = 0
    for item in reverse_dict(d)[0]:
        res += get_all_possible_hikes(d, item)
    return res


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def main():
    data = parse_data(test_data_01)
    print(data)
    print(reverse_dict(data)[0])
    show_map(get_hiking_trails_for_position(data, reverse_dict(data)[0][3]), size=10)
    print((get_all_possible_hikes(data, reverse_dict(data)[0][3])))

    # print(f"Testing Part 1: {part1(test_data_01)}")
    # file_data = get_file_data("./data/010.txt")
    # print(f"Part 1: {part1(file_data)}")  # 459

    print(f"Testing Part 2: {part2(test_data_01)}")
    file_data = get_file_data("./data/010.txt")
    print(f"Part 2: {part2(file_data)}")


if __name__ == "__main__":
    main()
