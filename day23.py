import re
import os

from collections import namedtuple
from typing import List

Vec = namedtuple('Vec', 'x, y, z')
Bot = namedtuple('Bot', 'pos, r')


def manhattan(v1: Vec, v2: Vec) -> int:
    """
    Returns the Manhattan distance between two coordinates
    """
    return abs(v1.x - v2.x) + abs(v1.y - v2.y) + abs(v1.z - v2.z)


def parse_bots(lines: List[str]) -> List[Bot]:
    """
    Parses the input and returns a list of Bots
    """
    bots: List[Bot] = []
    pattern = r'pos=<(.+?),(.+?),(.+?)>, r=(\d+)'
    for line in lines:
        x, y, z, radius = re.match(pattern, line).groups()
        pos = Vec(*[int(scalar) for scalar in (x, y, z)])
        bots.append(Bot(pos, int(radius)))
    return bots


def bots_at(pos: Vec, bots: List[Bot]) -> int:
    """
    Returns the amount of bots in range at position
    """
    return len([bot for bot in bots if manhattan(pos, bot.pos) <= bot.r])


def best_point(bots: List[Bot]) -> int:
    """
    Finds the point with most bots in range of the point while keeping
    the distance from origin to a minimum.

    The algorithm is a hill climbing algorithm which starts at origin.
    It attempts to find a more dense part of the swarm by scanning at
    regular intervals around the current position. If a denser point is found,
    then it is set as the current position, added to a list and the search
    space formed by the intervals is halved. Then the process repeats until
    the search area is too small to continue further. At this point the list
    of the visited densest points can be sorted to find the point which was
    the most dense yet also closest to the origin.

    Note that this algorithm may get stuck in local optimum, i.e. it probably
    does not work for all possible inputs.
    """
    min_x, *_, max_x = sorted(bot.pos.x for bot in bots)
    min_y, *_, max_y = sorted(bot.pos.y for bot in bots)
    min_z, *_, max_z = sorted(bot.pos.z for bot in bots)

    origin = Vec(0, 0, 0)
    size = (max_x - min_x)  # Size of the search area and search density
    current = origin  # Start at origin
    best_points = []  # Densest points
    next_pos = origin
    most_bots = 0

    while size > 1:

        # Sample around the current position at regular intervals
        for x in range(-size, size, size // 2):
            for y in range(-size, size, size // 2):
                for z in range(-size, size, size // 2):

                    pos = Vec(current.x + x, current.y + y, current.z + z)
                    bot_count = bots_at(pos, bots)

                    # New best position found, keep track of it
                    if bot_count >= most_bots:
                        most_bots = bot_count
                        next_pos = pos
                        best_points.append(pos)

        current = next_pos
        size //= 2
        print(f'Bots at {current}: {most_bots}')

    # From the found best points find the one closest to origin
    best_points.sort(key=lambda point: manhattan(point, origin))
    best_points.sort(key=lambda point: bots_at(point, bots))
    return manhattan(best_points[-1], origin)


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day23.in')) as f:
        lines = f.read().splitlines()

    bots = parse_bots(lines)

    """
    First puzzle is trivial - just parse the input and figure out how many
    bots are in range of the strongest nanobot
    """
    largest = max(bots, key=lambda bot: bot.r)
    in_range = [b for b in bots if manhattan(largest.pos, b.pos) < largest.r]
    assert len(in_range) == 172

    """
    Second part is sort of tricky. The solution here uses a hill climbing
    algorithm, i.e. it steps towards a "denser" part of the nanobot swarm
    and decreases the size of the step after each step. It seems to work for
    this input but there's a high chance that the solution could actually
    get stuck in a local optimum and never find the global optimum.
    """
    assert best_point(bots) == 125532607
