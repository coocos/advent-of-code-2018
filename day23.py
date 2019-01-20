import re
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

    bots: List[Bot] = []
    pattern = r'pos=<(.+?),(.+?),(.+?)>, r=(\d+)'
    for line in lines:
        x, y, z, radius = re.match(pattern, line).groups()
        pos = Vec(*[int(scalar) for scalar in (x, y, z)])
        bots.append(Bot(pos, int(radius)))
    return bots


if __name__ == '__main__':

    with open('day23.in') as f:
        lines = f.read().splitlines()

    bots = parse_bots(lines)

    # Figure out how many bots are in range of the strongest nanobot
    bots_in_range = 0
    strongest_bot = sorted(bots, key=lambda bot: bot.r)[-1]
    for bot in bots:
        if manhattan(strongest_bot.pos, bot.pos) <= strongest_bot.r:
            bots_in_range += 1
    assert bots_in_range == 172
