from typing import List, Generator, Set


def read_frequencies(filename: str) -> List[int]:
    """
    Reads frequencies from the input file and returns a list of them
    """
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


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

    data = read_frequencies('day1.in')

    final_frequency = 0
    for frequency in apply_frequencies(data):
        final_frequency = frequency

    print(f'Final frequency: {final_frequency}')

    current_frequency = 0
    previous_frequencies: Set[int] = set()
    duplicate_frequency = None

    while duplicate_frequency is None:
        for frequency in apply_frequencies(data, current_frequency):
            current_frequency = frequency
            if current_frequency in previous_frequencies:
                duplicate_frequency = current_frequency
                break
            previous_frequencies.add(current_frequency)

    print(f'First duplicate frequency: {duplicate_frequency}')
