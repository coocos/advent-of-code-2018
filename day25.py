from collections import namedtuple

Point = namedtuple('Point', 'x, y, z, w')


def manhattan(p1: Point, p2: Point) -> int:
    """
    Returns the Manhattan distance between two points
    """
    return (abs(p2.x - p1.x) +
            abs(p2.y - p1.y) +
            abs(p2.z - p1.z) +
            abs(p2.w - p1.w))


class Constellations:
    """
    Union find implementation for finding the constellations.
    """
    def __init__(self, n):
        self._identifiers = list(range(n))

    def union(self, x: int, y: int) -> None:
        """Joins x and y together"""
        previous_identifier = self._identifiers[x]
        new_identifier = self._identifiers[y]
        for i, identifier in enumerate(self._identifiers):
            if identifier == previous_identifier:
                self._identifiers[i] = new_identifier

    @property
    def count(self):
        """Returns the amount of constellations"""
        return len(set(self._identifiers))


if __name__ == '__main__':

    with open('day25.in') as f:
        points = [Point(*map(int, line.strip().split(','))) for line in f]

    constellations = Constellations(len(points))

    # Loop through all point pairs and join them if they're close enough
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            if manhattan(points[i], points[j]) <= 3:
                constellations.union(i, j)

    assert constellations.count == 428
