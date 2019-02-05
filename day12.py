import os

from typing import List, Dict, Deque
from collections import deque


Rules = Dict[str, str]


def parse_rules(raw_rules: List[str]) -> Rules:
    """
    Parses a rule-result dictionary from the raw string representation
    """
    rules = {}
    for rule in raw_rules:
        match, product = rule.split(' => ')
        rules[match] = product
    return rules


def iterate(state: str, rules: Rules) -> str:
    """
    Applies rules to the state of the automata and produces the next state
    """
    next_gen: List[str] = []

    # Pad the state so that edges of the state will also be checked
    state = '.' * 10 + state + '.' * 10

    for i in range(len(state)):
        pot = state[i - 2:i + 3]
        if pot in rules:
            next_gen.append(rules[pot])
        else:
            next_gen.append('.')
    return ''.join(next_gen)


def sum_pots(pots: str, offset: int) -> int:
    """
    Sums the pots according to their position. Offset indicates which
    pot is the "zero" pot.
    """
    return sum([i - offset if p == '#' else 0 for i, p in enumerate(pots)])


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day12.in')) as f:
        scenario = f.read().splitlines()

    pots = scenario[0].split(': ')[-1]
    rules = parse_rules([rule for rule in scenario[2:] if rule])
    generations = 50_000_000_000
    sums: List[int] = []  # Pot sums for each generation
    diffs: Deque[int] = deque(maxlen=5)  # Delta sums for last 5 generations

    for i in range(1, generations + 1):

        try:
            print(f'{i}: {sums[-1]} {sums[-1] - sums[-2]}')
        except IndexError:
            pass

        pots = iterate(pots, rules)
        sums.append(sum_pots(pots, i * 10))

        # Find the first generation after the 20th which is stable
        if len(sums) >= 20:
            diffs.append(sums[-1] - sums[-2])

            # If the last 5 generations all have the same diff then the
            # automata has converged to a stable state
            if len(diffs) == 5 and len(set(diffs)) == 1:
                print('Solution has converged')
                break

    # First half of the puzzle
    assert sums[19] == 2930

    """
    The second half of the puzzle is a bit trickier because the amount of
    generations is so large that it's not feasible to actually compute it.
    Instead the problem can be solved by observing that the automata converges
    to a stable state after around 100 generations. From that point on the sum
    the of the pots will increase by a constant for each generation. Therefore
    the puzzle can be solved by finding the sum and and constant increment of
    the first generation which is stable. Then the sum of the pots after fifty
    billion generations is:

    result = generation_sum + (50_000_000_000 - generation) * increment
    """
    assert (generations - i) * diffs[0] + sums[i-1] == 3099999999491
