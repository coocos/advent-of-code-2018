import string
import re
from typing import List, Tuple


def trigger_reactions(polymer: str) -> str:
    """
    Triggers the polymer reactions and returns the polymer with all the
    reactions applied.

    The algorithm works by iterating through the polymer and comparing the
    current unit against the next unit. If the next unit is the same as
    the current one but differ in capitalization then they are removed from
    the string and the algorithm starts again but this time one unit earlier
    than the current position.
    """
    i = 0
    while i < len(polymer) - 1:
        if polymer[i].lower() == polymer[i + 1].lower():
            if ((polymer[i].isupper() and polymer[i + 1].islower()) or
                    (polymer[i].islower() and polymer[i + 1].isupper())):
                    polymer = polymer[:i] + polymer[i + 2:]
                    i -= 1
                    continue
        i += 1

    return polymer


if __name__ == '__main__':

    with open('day5.in') as f:

        complex_polymer = f.read()

        # Solve first half of the puzzle - the -1 is due to newline
        assert len(trigger_reactions(complex_polymer)) - 1 == 11814

        # Solve second half of the puzzle by removing units alphabetically
        # and finding the smallest polymer after reactions have been applied
        polymers: List[Tuple[str, int]] = []
        for char in string.ascii_lowercase:
            polymer = re.sub(f'[{char}{char.upper()}]', '', complex_polymer)
            polymers.append((char, len(trigger_reactions(polymer)) - 1))
        assert min(polymers, key=lambda x: x[1]) == ('g', 4282)
