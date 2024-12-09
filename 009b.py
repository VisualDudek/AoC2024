import copy

data_test = "2333133121414131402"


def parse(data: str):
    is_digit = True
    lst = []
    id = 0
    for i, c in enumerate(data):
        if is_digit:
            lst.append((id, int(c)))
            id += 1
            is_digit = False
        else:
            lst.append((".", int(c)))
            is_digit = True
    return lst


def move(lst: list) -> list:
    idx = len(lst) - 1
    while idx > 0:
        # show(lst)
        # take only ID not "."
        if lst[idx][0] == "." or lst[idx][1] == 0:
            idx -= 1
            continue
        for i in range(idx):
            if lst[i][0] == "." and lst[i][1] >= lst[idx][1]:
                space_left = lst[i][1] - lst[idx][1]
                moving = lst[idx][0]
                lst[i] = (".", space_left)
                lst[idx] = (".", lst[idx][1])
                lst = lst[:i] + [(moving, lst[idx][1])] + lst[i:]
                idx += 1
                break

        idx -= 1

    return lst


def find_space(lst: list, n: int):
    running = 0
    for i, c in enumerate(lst):
        if c == ".":
            running += 1
        else:
            running = 0

        if running == n:
            return i - n + 1
    return False


def show(lst: list) -> None:
    for c, n in lst:
        print(str(c) * n, end="")
    print()


def parse_lst(lst: list) -> list:
    res = []
    for c, n in lst:
        res += [c] * n
    return res


def calculate(lst: list) -> int:
    res = 0
    for i, id in enumerate(lst):
        if id == ".":
            continue
        res += i * id
    return res


def main(data: str) -> None:
    # print(parse(data))
    # print((move(parse(data))))
    # print((move(parse(data))))
    print(calculate(parse_lst(move(parse(data)))))


if __name__ == "__main__":

    with open("./data/009.txt", "r") as f:
        data_file = f.read()

    data = data_test
    data = data_file
    main(data)
