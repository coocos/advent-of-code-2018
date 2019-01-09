from collections import namedtuple
from typing import List, Callable, Set

Registers = List[int]
Instruction = namedtuple('Instruction', 'code, a, b, c')


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

    opcodes = [
        addr,
        addi,
        mulr,
        muli,
        banr,
        bani,
        borr,
        bori,
        setr,
        seti,
        gtir,
        gtri,
        gtrr,
        eqir,
        eqri,
        eqrr
    ]

    with open('day16.in') as data:
        captured_samples, program = data.read().split('\n\n\n\n')

    # Parse captured samples
    samples: List[List] = []
    sample: List = []
    for line in captured_samples.splitlines():
        if line:
            if line.startswith('B'):
                # eval is evil but this ain't production
                sample.append(eval(line[7:]))
            elif line.startswith('A'):
                sample.append(eval(line[6:]))
                samples.append(sample)
                sample = []
            else:
                registers = [int(register) for register in line.split()]
                sample.append(Instruction(*registers))

    # Map of which opcodes are possible for values 0 - 15 - initially all are
    possible_ops = {x: set(opcodes) for x in range(16)}

    """
    Go through all samples and keep track of how many samples match how many
    opcodes and remove any opcode from possible_ops collection if the opcode
    does not produce the expected registers
    """
    ambiguous_opcodes = 0
    for sample in samples:
        matching_opcodes = 0
        for opcode in opcodes:
            register, instruction, expected = sample
            if opcode(instruction, register[:]) == expected:
                matching_opcodes += 1
            elif opcode in possible_ops[instruction.code]:
                possible_ops[instruction.code].remove(opcode)
        if matching_opcodes >= 3:
            ambiguous_opcodes += 1

    assert ambiguous_opcodes == 618

    """
    Several possible opcodes are still left for each identifier from 0 - 15 so
    find the ones which have only one possible opcode left. These opcodes have
    been uniquely defined so remove those opcodes from other possible opcode
    identifiers until each opcode identifier has a single opcode left.
    """
    while any(len(ops) > 1 for ops in possible_ops.values()):
        reserved_ops: Set[Callable] = set()
        for ops in possible_ops.values():
            if len(ops) == 1:
                reserved_ops = reserved_ops | ops
        for ops in possible_ops.values():
            if len(ops) > 1:
                ops.difference_update(reserved_ops)
    # Final opcode map where each value maps to a single opcode
    found_ops = {code: fns.pop() for code, fns in possible_ops.items()}

    # Run test program
    state: Registers = [0, 0, 0, 0]
    instructions = [[int(r) for r in l.split()] for l in program.splitlines()]
    for instruction in instructions:
        found_ops[instruction[0]](Instruction(*instruction), state)

    assert state == [514, 514, 2, 3]
