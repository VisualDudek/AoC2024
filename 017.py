import re
from typing import Dict


test_data_001 = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0"""


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
    i = 0
    while i < len(program):

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
        if opcode == 0:  # adv
            value = registers["A"] / 2**operand_value
            registers["A"] = int(value)
        elif opcode == 1:  # bxl
            value = registers["B"] ^ operand_value
            registers["B"] = value
        elif opcode == 2:  # bst
            registers["B"] = operand_value % 8
        elif opcode == 3:  # jnz
            if registers["A"] != 0:
                i = operand_value
                continue
        elif opcode == 4:  # bxc
            registers["B"] = registers["B"] ^ registers["C"]
        elif opcode == 5:  # out
            output.append(operand_value % 8)
        elif opcode == 6:  # bdv
            value = registers["A"] / 2**operand_value
            registers["B"] = int(value)
        elif opcode == 7:  # cdv
            value = registers["A"] / 2**operand_value
            registers["C"] = int(value)

        i += 2
    return output


def get_file_data(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()


def part1(data: str) -> int:
    registers, program = parse_data(data)
    res = run_program(registers, program)
    return ",".join(map(str, res))


def test():
    reg, prog = parse_data(test_data_001)
    print(reg)
    print(prog)
    res = run_program(reg, prog)
    print(",".join(map(str, res)))


if __name__ == "__main__":
    # test()
    data = get_file_data("./data/017.txt")
    print(part1(data))  # 7,1,5,2,4,0,7,6,1
