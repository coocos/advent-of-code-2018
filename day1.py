import os
from typing import List, Generator, Set


def apply_frequencies(frequencies: List[int], start: int = 0) -> Generator[int, None, None]:
    """
    Applies frequencies from the list to the starting frequency and yields
    the next frequency until the list is exhausted
    """
    total = start
    for frequency in frequencies:
        total += frequency
        yield total


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day1.in')) as f:
        data = [int(line) for line in f]

    # Find the final frequency
    final_frequency = 0
    for frequency in apply_frequencies(data):
        final_frequency = frequency

    assert final_frequency == 479

    current_frequency = 0
    previous_frequencies: Set[int] = set()
    duplicate_frequency = None

    # Find the first duplicate frequency
    while duplicate_frequency is None:
        for frequency in apply_frequencies(data, current_frequency):
            current_frequency = frequency
            if current_frequency in previous_frequencies:
                duplicate_frequency = current_frequency
                break
            previous_frequencies.add(current_frequency)

    assert duplicate_frequency == 66105
