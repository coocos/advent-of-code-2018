import os

from collections import namedtuple, defaultdict
from typing import List, Tuple, DefaultDict


Coord = namedtuple('Coord', 'x, y')


def manhattan(first: Coord, second: Coord) -> int:
    """
    Returns the Manhattan distance between two coordinates
    """
    return abs(first.x - second.x) + abs(first.y - second.y)


def closest(coord: Coord, coords: List[Coord]) -> Tuple[Coord, bool]:
    """
    Returns the closest known coordinate to this coordinate and a flag
    which indicates whether there are multiple closest coordinates
    """
    # Find the closest known coordinate for this coordinate
    distances = {}
    for target in coords:
        distances[target] = manhattan(coord, target)
    closest, min_distance = min(distances.items(), key=lambda c: c[1])

    count = 0
    # Check if coordinate is shared with multiple other coordinates
    for _, distance in distances.items():
        if distance == min_distance:
            count += 1
        if count > 1:
            return closest, True

    return closest, False


def largest_finite_area(coords: List[Coord]) -> int:
    """
    Returns the size of the largest finite area formed by the coordinates
    """
    # Find the boundaries of the known coordinate space
    max_x: int = max(coords, key=lambda coord: coord.x).x
    max_y: int = max(coords, key=lambda coord: coord.y).y

    areas: DefaultDict[Coord, List] = defaultdict(list)
    reserved = set(coords)

    # Generate all areas and gather them to a dictionary grouped by
    # the closest known coordinate
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            coord = Coord(x, y)
            if coord in reserved:
                areas[coord].append(coord)
            else:
                closest_coord, shared = closest(coord, coords)
                if not shared:
                    areas[closest_coord].append(coord)

    """
    Find the largest finite area from the formed areas. Finite areas can be
    identified by the fact that they cannot contain coordinates on the edge
    of the known coordinate space, i.e. all coordinates they contain are
    between 0, 0 and max_x, max_y.
    """
    finite_areas = []
    for key, area in areas.items():
        finite = True
        for coord in area:
            if coord.x in (0, max_x) or coord.y in (0, max_y):
                finite = False
                break
        if finite:
            finite_areas.append(area)
    largest_area = max(finite_areas, key=lambda area: len(area))
    return len(largest_area)


def close_to_all(coord: Coord, coords: List[Coord], tolerance: int) -> bool:
    """
    Returns True if coordinate is within a specified distance to all known
    coordinates and False if not
    """
    return sum(manhattan(coord, target) for target in coords) < tolerance


def area_near_locations(coords: List[Coord], tolerance: int = 30) -> int:
    """
    Returns the size of the area which contains all coordinates within a
    specified distance to all known coordinates
    """
    max_x: int = max(coords, key=lambda coord: coord.x).x
    max_y: int = max(coords, key=lambda coord: coord.y).y

    area: List[Coord] = []
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            if close_to_all(Coord(x, y), coords, tolerance):
                area.append(Coord(x, y))
    return len(area)


if __name__ == '__main__':

    simple_coords = [
        Coord(1, 1),
        Coord(1, 6),
        Coord(8, 3),
        Coord(3, 4),
        Coord(5, 5),
        Coord(8, 9)
    ]
    assert largest_finite_area(simple_coords) == 17
    assert area_near_locations(simple_coords, 32) == 16

    with open(os.path.join('inputs', 'day6.in')) as f:
        coords = [Coord(*map(int, line.split(', '))) for line in f]

    assert largest_finite_area(coords) == 2342
    assert area_near_locations(coords, 10000) == 43302
