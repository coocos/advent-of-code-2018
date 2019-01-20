from collections import namedtuple
from typing import List

Registers = List[int]
Instruction = namedtuple('Instruction', 'a, b, c')


def addr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] + registers[op.b]
    return registers


def addi(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] + op.b
    return registers


def mulr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] * registers[op.b]
    return registers


def muli(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] * op.b
    return registers


def banr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] & registers[op.b]
    return registers


def bani(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] & op.b
    return registers


def borr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] | registers[op.b]
    return registers


def bori(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a] | op.b
    return registers


def setr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = registers[op.a]
    return registers


def seti(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = op.a
    return registers


def gtir(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(op.a > registers[op.b])
    return registers


def gtri(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(registers[op.a] > op.b)
    return registers


def gtrr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(registers[op.a] > registers[op.b])
    return registers


def eqir(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(op.a == registers[op.b])
    return registers


def eqri(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(registers[op.a] == op.b)
    return registers


def eqrr(op: Instruction, registers: Registers) -> Registers:
    registers[op.c] = int(registers[op.a] == registers[op.b])
    return registers


if __name__ == '__main__':

    with open('day19.in') as f:
        lines = f.read().splitlines()

    pc = int(lines[0][-1])  # Which register the program counter is stored in
    registers: Registers = [0, 0, 0, 0, 0, 0]

    # Parse instructions
    instructions = []
    for line in lines[1:]:
        op, *values = line.split()
        # This ain't production, eval is just fine and dandy
        instructions.append((eval(op), Instruction(*[int(v) for v in values])))

    # Execute the program
    try:
        while True:
            op, instruction = instructions[registers[pc]]
            op(instruction, registers)
            registers[pc] += 1
    # IndexError will be thrown once the background process halts
    except IndexError:
        pass
    assert registers[0] == 878

    """
    The second part of the program will take too long to execute, at least
    when using Python. An alternative solution suggested on Reddit is to
    study the instructions and figure out what the program actually does.
    I've provided a breakdown @ day19_explained.md but the gist of the program
    is trying to find the sum of products of the value stored in register 2.
    As the second part of the puzzle stores 10551277 in register 2, this
    solution just computes the sum of products for that value using Python
    instead of elfcode:
    """
    value = 10551277
    sum_of_products = sum(x for x in range(1, value + 1) if value % x == 0)
    assert sum_of_products == 11510496
