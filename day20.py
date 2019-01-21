from collections import defaultdict, namedtuple, deque
from typing import List, DefaultDict, Deque, Tuple

Vec = namedtuple('Vec', 'x, y')


def create_grid(regex: str) -> DefaultDict:
    """
    Parses the regex and creates a two-dimensional grid representing
    the map layout.

    The regular expression is parsed by pushing the current position to the
    stack whenever '(' is encountered and popping it from the stack whenever
    ')' is encountered. If '|' is encountered, i.e. the solution branches out,
    then the current position is set to position at the top of the stack but
    the stack is not popped as the position is also the starting point for the
    other branches.
    """
    grid: DefaultDict = defaultdict(lambda: defaultdict(lambda: '#'))
    position = Vec(0, 0)
    positions: List[Vec] = [position]

    for char in regex:
        if char in '^$':
            continue
        elif char == 'E':
            grid[position.y][position.x + 1] = '|'
            position = Vec(position.x + 2, position.y)
        elif char == 'N':
            grid[position.y - 1][position.x] = '-'
            position = Vec(position.x, position.y - 2)
        elif char == 'W':
            grid[position.y][position.x - 1] = '|'
            position = Vec(position.x - 2, position.y)
        elif char == 'S':
            grid[position.y + 1][position.x] = '-'
            position = Vec(position.x, position.y + 2)
        elif char == '(':
            positions.append(position)
        elif char == ')':
            position = positions.pop()
        elif char == '|':
            position = positions[-1]
        grid[position.y][position.x] = '.'
    return grid


def number_of_doors(grid: DefaultDict) -> Tuple[int, int]:
    """
    Finds the distances to each room via breadth-first search and returns
    the amount of doors on the shortest route to the the farthest room,
    as well as the amount of rooms which are located at least 1000 doors away.
    """
    queue: Deque = deque([Vec(0, 0)])  # Queue of unvisited rooms

    # Keep a dictionary of rooms and their distances from the origin
    distances: DefaultDict = defaultdict(lambda: defaultdict(int))
    distances[0][0] = 0

    most_distant = 0  # How many doors to the most distant room
    distant_rooms = 0  # Amount of rooms over 1000 doors away

    while queue:

        room = queue.popleft()
        distance_to_this_room = distances[room.y][room.x] + 1

        # Possible door directions and the rooms next to them
        left = (Vec(room.x - 1, room.y), Vec(room.x - 2, room.y))
        right = (Vec(room.x + 1, room.y), Vec(room.x + 2, room.y))
        top = (Vec(room.x, room.y - 1), Vec(room.x, room.y - 2))
        bottom = (Vec(room.x, room.y + 1), Vec(room.x, room.y + 2))

        # Visit neighbouring rooms and update their distances
        for neighbor, room in (left, right, top, bottom):
            if grid[neighbor.y][neighbor.x] in '|-':
                if distances[room.y][room.x] == 0:
                    distances[room.y][room.x] = distance_to_this_room
                    if distance_to_this_room > most_distant:
                        most_distant = distance_to_this_room
                    if distance_to_this_room >= 1000:
                        distant_rooms += 1
                    queue.append(room)

    return most_distant, distant_rooms


if __name__ == '__main__':

    with open('day20.in') as f:
        regex = f.read()

    grid = create_grid(regex)
    most_distant, distant_rooms = number_of_doors(grid)
    assert most_distant == 4501
    assert distant_rooms == 8623
