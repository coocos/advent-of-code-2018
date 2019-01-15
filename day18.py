from copy import deepcopy
from itertools import chain
from typing import List


def surrounding_acres(x: int, y: int, acres: List[List[str]]) -> List[str]:
    """
    Returns the acres surrounding (x, y)
    """
    surrounding: List[str] = []
    neighbors = [
        (x - 1, y - 1), (x, y - 1), (x + 1, y - 1),
        (x - 1, y), (x + 1, y),
        (x - 1, y + 1), (x, y + 1), (x + 1, y + 1)
    ]

    for neighbor in neighbors:
        # Python is unfortunately too helpful by supporting negative indexing
        # so omit negative indices manually
        if neighbor[0] >= 0 and neighbor[1] >= 0:
            try:
                surrounding.append(acres[neighbor[1]][neighbor[0]])
            except IndexError:
                pass
    return surrounding


def transform_acre(x: int, y: int, acres: List[List[str]]) -> str:
    """
    Applies transformation rules to a single acre
    """
    acre = acres[y][x]
    surrounding = surrounding_acres(x, y, acres)

    # Open ground
    if acre == '.' and surrounding.count('|') >= 3:
        return '|'
    # Tree
    elif acre == '|' and surrounding.count('#') >= 3:
        return '#'
    # Lumberyard
    elif acre == '#' and (surrounding.count('#') < 1 or surrounding.count('|') < 1):
        return '.'
    return acre


def transform(acres: List[List[str]]) -> List[List[str]]:
    """
    Transforms acres to the acres after 1 minute
    """
    future_acres = deepcopy(acres)
    for y, acre_row in enumerate(acres):
        for x, acre in enumerate(acre_row):
            future_acres[y][x] = transform_acre(x, y, acres)

    return future_acres


def resource_value(acres: List[List[str]]) -> int:
    """
    Returns the resource value of the acres
    """
    flattened_acres = list(chain(*acres))
    trees = flattened_acres.count('|')
    lumberyards = flattened_acres.count('#')
    return trees * lumberyards


if __name__ == '__main__':

    with open('day18.in') as f:
        input_lines = f.read().splitlines()

    acres = [list(line) for line in input_lines]

    # Solve first part by running the simulation for 10 minutes
    for _ in range(10):
        acres = transform(acres)
    assert resource_value(acres) == 543312

    """
    The second part can be solved by observing how the automata behaves
    since a pure simulation takes too long to run. The automata actually
    starts repeating after several hundred iterations, e.g. iterations
    581, 609, and 637 are visually the same. That means the pattern
    repeats after 28 iterations so you can first iterate the simulation
    to a point where the automata is stable (i.e. when it starts to repeat
    in cycles). Then you can compute how many cycles there are before the
    10,000,000,00th iteration, skip those cycles and just iterate the
    remaining iterations.
    """
    acres = [list(line) for line in input_lines]  # Reset acres

    # Progress to an iteration where the automata is guaranteed to be stable
    for i in range(1, 582):
        acres = transform(acres)

    # Compute how many cycles we can skip and skip them
    iterations = (10_000_000_00 - i) % 28
    for i in range(iterations):
        acres = transform(acres)

    # Draw a pretty picture of the automata
    for acre_row in acres:
        print(''.join(acre_row))

    assert resource_value(acres) == 199064
