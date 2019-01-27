import re
from math import inf
from heapq import heappush, heappop
from typing import List, Any


def create_cave(depth: int, tx: int, ty: int) -> List[List[int]]:
    """
    Creates the cave according to the cave generation rules.

    Since the cave is essentially infinite a constant size padding is applied
    around the target coordinates to make the pathfinding feasible. Note that
    there needs to be a padding because the optimal path can overshoot the
    target. The padding size for this input was found simply by starting with
    a very large value and progressively decreasing it until a value small
    enough was found which produces the correct pathfinding result but is
    still relatively quick to compute.
    """
    PADDING = 50
    cave = [[0] * (tx + PADDING) for _ in range(ty + PADDING)]

    for y in range(ty + PADDING):
        for x in range(tx + PADDING):
            index = None
            if y == 0 and x == 0:
                index = 0
            elif y == 0:
                index = x * 16807
            elif x == 0:
                index = y * 48271
            elif y == ty and x == tx:
                index = 0

            if index is None:
                cave[y][x] = (cave[y-1][x] * cave[y][x-1] + depth) % 20183
            else:
                cave[y][x] = (index + depth) % 20183

    return cave


def risk_level(cave: List[List[int]], tx: int, ty: int) -> int:
    """
    Computes risk level for the smallest rectangle which contains both the
    mouth of the cave and the target.
    """
    risk_level = 0
    for y in range(ty + 1):
        for x in range(tx + 1):
            risk_level += cave[y][x] % 3
    return risk_level


def allowed(tool: str, region: str):
    """
    Returns whether tool is allowed at region.
    """
    # Rocky
    if region == '.':
        return tool in ('t', 'c')
    # Wet
    elif region == '=':
        return tool in ('c', 'n')
    # Narrow
    else:
        return tool in ('t', 'n')


def dijkstra(grid: List[List[Any]], tx: int, ty: int) -> int:
    """
    Dijkstra's algorithm applied to the problem of finding the shortest
    path to the target via optimal tool selection.

    The algorithm works exactly like the regular Dijkstra's algorithm with a
    priority queue but it needs to keep track of the equipped tool in addition
    to the distance to each node as the distance to each node depends on the
    tools used to reach that node.
    """
    # Convert erosion levels to terrain types for easier visualization
    types = ('.', '=', '|')
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x] = types[grid[y][x] % 3]

    q = []  # Queue of (distance, x, y, tool)
    heappush(q, (0, 0, 0, 't'))  # Start at the mouth of the cave
    distances = {(0, 0, 't'): 0}  # Distance to each node with specified tool
    neighbours = ((0, -1), (1, 0), (0, 1), (-1, 0))  # Neighbour vectors

    # Apply Dijkstra and find the shortest route to the target
    while q:

        distance, x, y, tool = heappop(q)

        for nx, ny in ((x + nx, y + ny) for nx, ny in neighbours):
            if nx >= 0 and ny >= 0 and nx < len(grid[0]) and ny < len(grid):

                for new_tool in ('t', 'c', 'n'):

                    # Tool needs to be valid both here and next door
                    if allowed(tool, grid[ny][nx]) and \
                       allowed(tool, grid[y][x]):

                        # Current tool can be kept - no time penalty
                        if new_tool == tool:
                            neighbour_dist = 1
                        # Current tool needs to be swapped - time penalty
                        else:
                            neighbour_dist = 8
                        neighbour_dist += distance

                        triple = (ny, nx, new_tool)
                        if neighbour_dist < distances.get(triple, inf):
                            distances[triple] = neighbour_dist
                            heappush(q, (neighbour_dist, nx, ny, new_tool))

    return distances.get((ty, tx, 't'))


if __name__ == '__main__':

    data = 'depth: 4845 target: 6,770'
    pattern = r'depth: (\d+) target: (\d+),(\d+)'
    match = re.match(pattern, data)
    depth, tx, ty = (int(v) for v in match.groups())

    cave = create_cave(depth, tx, ty)
    assert risk_level(cave, tx, ty) == 5400
    assert dijkstra(cave, tx, ty) == 1048
