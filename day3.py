import re
import os

from collections import namedtuple
from typing import Any, Tuple, List, Set


Claim = namedtuple('Claim', 'id, area')
Coordinate = Tuple[int, int]


def read_claims(filename: str) -> Any:
    """
    Reads the claims from a file and returns them as a list
    """
    with open(os.path.join('inputs', filename)) as f:
        return f.read().splitlines()


def parse_claim(claim: str) -> Claim:
    """
    Parses claim and returns it as a Claim
    """
    regex = r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)'
    match = re.match(regex, claim)
    x1, x2 = int(match.group(2)), int(match.group(2)) + int(match.group(4))
    y1, y2 = int(match.group(3)), int(match.group(3)) + int(match.group(5))

    # Generate all the "spots" the claim contains
    area = set()
    for x in range(x1, x2):
        for y in range(y1, y2):
            area.add((x, y))

    return Claim(int(match.group(1)), area)


def intersect_claims(claims: List[Claim]) -> Tuple[Set[Coordinate], Set[str]]:
    """
    Brute-force algorithm for discovering all the overlapping areas between
    different claims. Returns a set of coordinates which overlap between one
    or more claims and set of claims which do not overlap at all.

    The algorithm simply compares each claim against the claims after it and
    intersects the areas against each other. As each area is a set of
    coordinates the intersection is trivial albeit the algorithm is quite slow.
    """
    not_intersected: Set[str] = set(claim.id for claim in claims)
    intersections: Set[Coordinate] = set()

    for i, first_claim in enumerate(claims):
        for second_claim in claims[i + 1:]:
            intersected_area = first_claim.area & second_claim.area
            if intersected_area:
                intersections.update(intersected_area)
                if first_claim.id in not_intersected:
                    not_intersected.remove(first_claim.id)
                if second_claim.id in not_intersected:
                    not_intersected.remove(second_claim.id)
    return intersections, not_intersected


if __name__ == '__main__':

    simple_data = [
        '#1 @ 1,3: 4x4',
        '#2 @ 3,1: 4x4',
        '#3 @ 5,5: 2x2'
    ]
    claims = [parse_claim(claim) for claim in simple_data]
    intersections, not_intersected = intersect_claims(claims)
    assert len(intersections) == 4
    assert not_intersected == {3}

    claims = [parse_claim(claim) for claim in read_claims('day3.in')]
    intersections, not_intersected = intersect_claims(claims)
    assert len(intersections) == 111630
    assert not_intersected == {724}
