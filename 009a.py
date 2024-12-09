data_test = "2333133121414131402"


def parse(data: str):
    lst = []
    stack = []
    is_block = True
    id = 0
    for c in data:
        if is_block:
            for _ in range(int(c)):
                lst.append(id)
                stack.append(id)
            is_block = False
            id += 1
        else:
            for _ in range(int(c)):
                lst.append(".")
            is_block = True
    return lst, stack


def get_prev_digit(lst: list, idx: int) -> int:
    while not str(lst[idx]).isdigit():
        idx -= 1
    return idx


def move(lst: list) -> list:
    idx_end = len(lst) - 1
    idx_end = get_prev_digit(lst, idx_end)
    idx = 0
    while idx < idx_end:
        if lst[idx] == ".":
            lst[idx] = lst[idx_end]
            idx_end = get_prev_digit(lst, idx_end - 1)
            idx += 1
        else:
            idx += 1

    return lst[:idx]


def calculate(lst: list) -> int:
    res = 0
    for i, id in enumerate(lst):
        res += i * id
        # print(i, " ", id, " ", res)
    return res


def main(data: str) -> None:
    print(parse(data))
    lst, stack = parse(data)
    print(move(lst))
    lst, stack = parse(data)
    print(calculate(move(lst)))


if __name__ == "__main__":

    with open("./data/009.txt", "r") as f:
        data_file = f.read()

    data = data_test
    data = data_file
    main(data)
