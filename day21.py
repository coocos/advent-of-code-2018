from collections import namedtuple, deque
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

    with open('day21.in') as f:
        lines = f.read().splitlines()

    pc = int(lines[0][-1])  # Which register the program counter is stored in

    # Parse instructions
    instructions = []
    for line in lines[1:]:
        op, *values = line.split()
        # This ain't production, eval is just fine and dandy
        instructions.append((eval(op), Instruction(*[int(v) for v in values])))

    """
    The solution to the first half of the puzzle can be found by evaluating the
    input program. If you evaluate the program and observe which instructions
    touch register 0 then you'll notice that the program compares register 0
    with register 4 @ instruction 28. If the comparison is true, then the
    program counter will jump outside the application memory. So the solution
    to the first half of the puzzle is to store the value of register 4 when
    the register comparison is executed for the first time.

    The second half of the puzzle asks for the value of register 0 which halts
    the program after the most instructions. The key to is to understand that
    the register comparison sequence will eventually start from the beginning.
    Therefore the solution is to find the the _last_ value for register 4
    before the register comparison sequence starts from the beginning again.
    """

    registers = [0, 0, 0, 0, 0, 0]
    used_register_values = set()  # All register 4 values used in eqrr
    first_halt = None  # Register 0 value which halts first
    last_halt = None  # Register 0 value which halts last
    register_states = deque([], maxlen=2)  # Last 2 register values

    # Execute the program and find the register values which cause a halt
    while True:

        op, instruction = instructions[registers[pc]]
        op(instruction, registers)

        if op == eqrr:

            register_states.append(registers[4])

            """
            No register comparison has been executed so far so the current
            register 4 value is what will cause the program to halt after
            the fewest instructions
            """
            if not first_halt:
                first_halt = registers[4]

            """
            Register comparison has cycled so the register value used in
            the comparison previously is the value which causes the program
            to halt after the most instructions
            """
            if registers[4] in used_register_values:
                last_halt = register_states[0]
                break

            used_register_values.add(registers[4])
        registers[pc] += 1

    assert first_halt == 16128384
    assert last_halt == 7705368
