# What the input program does

The core of the program is spent on a nested loop. If it's converted
by hand into a higher-level language like Python it looks something
like this:

```python
r0 = 0

for r3 in range(1, 10551277 + 1):
    for r1 in range(1, 10551277 + 1):
        if r2 == r3 * r1:
            r0 += r3
```

r2 contains the constant initialized in the setup phase, i.e.
we are trying to find an r3 which multiplied with r1 equals
the constant. That sounds an awful lot like finding the products
of the constant. And more precisely, since r3 is always added to to r0, 
the program is trying to find the sum of products for the constant.
This also makes sense empirically since the first part of the puzzle
stored 877 in r2 and the correct solution was 878. 877 is a prime number
so its only products are 877 and 1 and 877 + 1 equals 878.

# Understanding the input program step by step

The program starts by setting the program counter to register 5.
After that it immediately jumps to the setup section at instruction
17:

```elfcode
#ip 5  # store program counter in register 5
0 addi 5 16 5  # jump to setup section (instruction 17)
```

The looping main logic follows. Note that this is run only after the setup
phases have been executed and it forms the higher-level loop described
above:

```
1 seti 1 7 3  # r3 = 1
2 seti 1 4 1  # r1 = 1

3 mulr 3 1 4  # r4 = r3 * r1
4 eqrr 4 2 4  # if r2 == r4 set r4 to 1 else 0
5 addr 4 5 5  # pc = pc + r4
6 addi 5 1 5  # pc = pc + 1
7 addr 3 0 0  # r0 = r0 + r3, i.e. increment the sum of found products
8 addi 1 1 1  # r1 = r1 + 1
9 gtrr 1 2 4  # if r1 > r2 set r4 to 1 else 0
10 addr 5 4 5  # pc = pc + r4
11 seti 2 1 5  # pc = 2, jump to 3
12 addi 3 1 3  # r3 = r3 + 1
13 gtrr 3 2 4  # if r3 > r2 set r4 to 1 else 0
14 addr 4 5 5  # pc = pc + r4, jump to r4
15 seti 1 4 5  # pc = 1, jump to 2

16 mulr 5 5 5  # pc = pc * pc (halts when it eventually reaches this instruction?)
```

What follows is the first setup section. The program immediately jumps here
and initializes register 2 with a value. Once it has done that it will
jump to the loop section (first part of the puzzle) or the second setup
section if register 0 contains 1 (second part of the puzzle):

```elfcode
17 addi 2 2 2  # r2 = r2 + 2
18 mulr 2 2 2  # r2 = r2 * r2
19 mulr 5 2 2  # r2 = pc * r2
20 muli 2 11 2  # r2 = r2 * 11
21 addi 4 1 4  # r4 = r4 + 1
22 mulr 4 5 4  # r4 = pc * r4
23 addi 4 19 4  # r4 = r4 + 19
24 addr 2 4 2  # r2 = r2 + r4, r2 = 877 (first part of the puzzle)
25 addr 5 0 5  # pc = pc + r0, jump to second setup if r0 = 1, else jump to main loop
26 seti 0 9 5  # pc = 0
```

Finally we have the second setup section. Only the second part of the puzzle executes
these instructions. Essentially these instructions just initialize register 2
with a larger value than the first setup section. The last instructions jumps to the
loop phase just like the first one.

```elfcode
27 setr 5 7 4  # r4 = pc
28 mulr 4 5 4  # r4 = pc * r4
29 addr 5 4 4  # r4 = pc + r4
30 mulr 5 4 4  # r4 = pc * r4
31 muli 4 14 4  # r4 = r4 * 14
32 mulr 4 5 4  # r4 = pc * r4
33 addr 2 4 2  # r2 += r4, r2 = 10551277 (second part of the puzzle)
34 seti 0 9 0  # r0 = 0
35 seti 0 6 5  # pc = 6, jump to 6
```
