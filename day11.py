from collections import defaultdict
from typing import Tuple, Optional

Answer = Tuple[int, int, int]


def power_level(x: int, y: int, serial_number: int) -> int:
    """
    Compute power level for fuel cell
    """
    rack_id = x + 10
    base_power = rack_id * y + serial_number
    base_power *= rack_id
    base_power = base_power // 100 % 100 % 10
    return base_power - 5


def largest_fuel_cell(serial: int, size: Optional[int] = None) -> Answer:
    """
    Finds the position and size of the area with the largest total fuel cell
    power level. If size is provided, then only areas of that size will be
    considered. If not, then all area sizes will be used to find the largest
    power level value.

    A data structure called a summed-area table (see definition @
    https://en.wikipedia.org/wiki/Summed-area_table) is used to to compute
    total power levels for various grid sizes as a pure brute-force solution
    proved to be very slow when searching for the optimal solution with all
    possible grid sizes in the second half of the puzzle. This algorithm could
    be further optimized to compute the grid search in parallel using the
    previously constructed summed-area table.
    """

    # Construct summed-area table
    table = defaultdict(lambda: defaultdict(int))
    for y in range(1, 300 + 1):
        for x in range(1, 300 + 1):
            cell_power = power_level(x, y, serial)
            table[x][y] = cell_power + table[x-1][y] + table[x][y-1] - table[x-1][y-1]

    # If area size is not provided then iterate over all grid sizes
    if size is None:
        low, high = 1, 300
    else:
        low, high = size, size + 1

    top_left_x, top_left_y = 0, 0
    optimal_size = size
    largest = 0

    # Find the largest area
    for size in range(low, high):
        for y in range(1, 300 + 1):
            for x in range(1, 300 + 1):
                power = table[x][y] - table[x-size][y] - table[x][y-size] + table[x-size][y-size]
                if power > largest:
                    top_left_x = x + 1 - size
                    top_left_y = y + 1 - size
                    optimal_size = size
                    largest = power

    return (top_left_x, top_left_y, optimal_size)


if __name__ == '__main__':

    # Solve first part of the puzzle
    assert largest_fuel_cell(7803, 3) == (20, 51, 3)
    assert largest_fuel_cell(18, 16) == (90, 269, 16)
    assert largest_fuel_cell(42, 12) == (232, 251, 12)

    # Solve second half of the puzzle
    assert largest_fuel_cell(18) == (90, 269, 16)
    assert largest_fuel_cell(42) == (232, 251, 12)
    assert largest_fuel_cell(7803) == (230, 272, 17)
