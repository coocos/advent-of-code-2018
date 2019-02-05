import re
import sys
import os

from typing import List, Tuple

"""
This particular solution is deeply recursive so defy all sane habits
and increase the recursion limit to a number which works
"""
sys.setrecursionlimit(5000)

Ground = List[List[str]]


def load_data(filename: str) -> Ground:
    """
    Parses the clay reservoirs from the input file and constructs a map of the
    ground
    """
    regex = r'([xy])=(\d+), ([xy])=(\d+)\.\.(\d+)'
    coords: List[Tuple[int, int]] = []

    with open(os.path.join('inputs', filename)) as f:
        for line in f:
            clay = re.match(regex, line)
            if clay[1] == 'x':
                for y in range(int(clay[4]), int(clay[5]) + 1):
                    coords.append((int(clay[2]), y))
            else:
                for x in range(int(clay[4]), int(clay[5]) + 1):
                    coords.append((x, int(clay[2])))

    # Find minimum and maximum clay reservoir coordinates
    horizontal = sorted(coords, key=lambda coord: coord[0])
    min_x, max_x = horizontal[0][0], horizontal[-1][0]
    max_y = max(coords, key=lambda coord: coord[1])[1]

    # Construct map and pad it so that water has space to overflow from sides
    ground = []
    for y in range(max_y + 1):
        ground.append(['.' for x in range(min_x - 1, max_x + 2)])

    # Move clay reservoirs to start horizontally at 0
    coords = [(c[0] - min_x + 1, c[1]) for c in coords]

    # Place clay reservoirs and spring
    for x, y in coords:
        ground[y][x] = '#'
    ground[0][501 - min_x] = '+'

    return ground


def is_overflowing(x: int, y: int, ground: Ground) -> bool:
    """
    Returns True if the water surface at (x, y) is overflowing from any
    part of the surface, False if not.
    """
    overflowing = False
    offset = 1
    # Check left side of the surface / stream
    while True:
        if ground[y][x - offset] == '|':
            overflowing = True
            break
        # Stream hit a clay reservoir so water cannot overflow from here
        elif ground[y][x - offset] == '#':
            break
        offset += 1
    offset = 1
    # Check right side of the surface / stream
    while True:
        if ground[y][x + offset] == '|':
            overflowing = True
            break
        # Stream hit a clay reservoir so water cannot overflow from here
        elif ground[y][x + offset] == '#':
            break
        offset += 1
    return overflowing


def spread(x: int, y: int, ground: Ground, direction: int) -> None:
    """
    Spreads the stream sideways to either left or right. If the stream spreads
    to a position where it should fall then the stream will start falling.
    """
    if ground[y][x] == '#':
        return
    elif ground[y + 1][x] == '.':
        ground[y][x] = '|'
        fall(x, y, ground)
    elif ground[y][x] == '.':
        ground[y][x] = '~'
        spread(x + direction, y, ground, direction)


def rise(x: int, y: int, ground: Ground) -> None:
    """
    Raises the water level and spreads the stream sideways if needed.
    """
    # Spread the water to fill the current level
    spread(x - 1, y, ground, -1)
    spread(x + 1, y, ground, 1)
    ground[y][x] = '~'

    # If the stream has not overflowed then it needs to rise
    if not is_overflowing(x, y, ground):
        rise(x, y - 1, ground)
    # This particular stream is now overflowing so water level will settle
    else:
        ground[y][x] = '~'


def fall(x: int, y: int, ground: Ground) -> None:
    """
    Follows the stream of water as it falls through the sand, spreading the
    water to the sides when clay reservoirs are encountered.
    """
    try:
        current = ground[y][x]

        # Start of the stream - just fall down
        if current == '+':
            ground[y + 1][x] = '|'
            fall(x, y + 1, ground)
        elif current == '|':
            # Stream falls to sand so it keeps falling
            if ground[y + 1][x] == '.':
                ground[y + 1][x] = '|'
                fall(x, y + 1, ground)
            # Streams falls to a clay reservoir so it spreads
            elif ground[y + 1][x] == '#':
                spread(x - 1, y, ground, -1)
                spread(x + 1, y, ground, 1)
                ground[y][x] = '~'
                # Rise only if spreading did not cause an overflow
                if not is_overflowing(x, y, ground):
                    rise(x, y - 1, ground)
            # The tricky case where stream flows into an already filled pool
            elif ground[y + 1][x] == '~':
                # Stream should die if pool is already overflowing
                if not is_overflowing(x, y, ground):
                    spread(x - 1, y, ground, -1)
                    spread(x + 1, y, ground, 1)
                    ground[y][x] = '~'
                    # Water level should rise if pool is still not overflowing
                    if not is_overflowing(x, y, ground):
                        rise(x, y - 1, ground)
    except IndexError:
        # Stream fell beneath the last visible level
        pass


if __name__ == '__main__':

    ground = load_data('day17.in')
    start = ground[0].index('+')
    fall(start, 0, ground)

    """
    Count how many tiles are reachable by water, i.e. how many tiles # are
    either '~' or '|' to solve the first puzzle
    """
    reachable_tiles = 0
    ignored = True
    for level in ground:
        # Water tiles above the first clay reservoir are ignored
        if '#' in level:
            ignored = False
        if not ignored:
            for tile in level:
                if tile in '~|':
                    reachable_tiles += 1

    assert reachable_tiles == 42429

    """
    Replace overflowing surfaces, i.e. surfaces like '|~~~~' with flowing
    streams like '|||||' to make it easier to count retained water tiles
    for the second part of the puzzle
    """
    pattern = r'\|([~]+)|([~]+)\|'
    retained_tiles = 0
    ground_str = ''.join(t for l in ground for t in l)
    row = re.sub(pattern, lambda m: m.group(0).replace('~', '|'), ground_str)
    retained_tiles += row.count('~')

    assert retained_tiles == 35998
