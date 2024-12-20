from functools import lru_cache
import re
from typing import Dict


test_data_001 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""

test_data_002 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0"""


def parse_data(s: str):
    registers: Dict[str, int] = {}
    it = iter(s.split("\n"))

    registers["A"] = int(next(it).split()[-1])
    registers["B"] = int(next(it).split()[-1])
    registers["C"] = int(next(it).split()[-1])

    next(it)

    digits = re.findall(r"\d+", next(it))
    program = [int(d) for d in digits]
    # this is the same as:
    # program = list(map(int, digits))

    return registers, program


def run_program(registers: Dict[str, int], program: list[int]):
    # for opcode, operand in zip(program[::2], program[1::2]):
    # for i in range(0, len(program), 2):
    output = []
    ouotput_max = len(program)
    i = 0
    while i < len(program):

        if output:
            if output[-1] != program[len(output) - 1]:
                break

        opcode = program[i]
        operand = program[i + 1]
        # deal with operand first
        if operand in (0, 1, 2, 3):
            operand_value = operand
        elif operand == 4:
            operand_value = registers["A"]
        elif operand == 5:
            operand_value = registers["B"]
        elif operand == 6:
            operand_value = registers["C"]
        else:
            raise ValueError("Invalid operand")

        # deal with opcode
        if opcode in (0, 1, 2, 4, 6, 7):  # jnz
            registers = fn_for_cache(
                registers["A"], registers["B"], registers["C"], opcode, operand_value
            )
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                i = operand_value
                continue
        elif opcode == 5:  # out
            output.append(operand_value % 8)

        i += 2
    return output


@lru_cache(maxsize=128)
def fn_for_cache(a, b, c, opcode, operand_value):
    if opcode == 0:  # adv
        value = a / 2**operand_value
        a = int(value)
    elif opcode == 1:  # bxl
        value = b ^ operand_value
        b = value
    elif opcode == 2:  # bst
        b = operand_value % 8
    elif opcode == 4:  # bxc
        b = b ^ c
    elif opcode == 6:  # bdv
        value = a / 2**operand_value
        b = int(value)
    elif opcode == 7:  # cdv
        value = a / 2**operand_value
        c = int(value)

    return {"A": a, "B": b, "C": c}


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def part1(data: str):
    registers, program = parse_data(data)
    res = run_program(registers, program)
    return ",".join(map(str, res))


def part2(data: str):
    registers, program = parse_data(data)

    seek = ",".join(map(str, program))

    for i in range(99_000_000, 200_000_000):
        if i % 1_000_000 == 0:
            print(f"{i:,}")
        registers["A"] = i
        res = run_program(registers, program)
        if ",".join(map(str, res)) == seek:
            return i
    return None


def test():
    reg, prog = parse_data(test_data_001)
    print(reg)
    print(prog)
    res = run_program(reg, prog)
    print(",".join(map(str, res)))


if __name__ == "__main__":
    # test()
    data = get_file_data("./data/017.txt")
    # print(part1(data))  # 7,1,5,2,4,0,7,6,1
    # print(part2(test_data_002))  # 117440

    print(part2(data))
