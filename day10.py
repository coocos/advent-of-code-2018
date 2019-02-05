import re
import sys
import os

from typing import List, Tuple


class Point:
    """
    A simple two-dimensional point with velocity
    """
    def __init__(self, x, y, vx=None, vy=None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def update(self):
        """
        Updates the point to a new position according to its velocity
        """
        self.x += self.vx
        self.y += self.vy

    def reverse(self):
        """
        Updates the point to its previous position according to its velocity
        """
        self.x -= self.vx
        self.y -= self.vy


def parse(raw_points: List[str]) -> List[Point]:
    """
    Parses list of strings into a list of Points
    """
    points = []
    regex = r'position=<\s?(?:(-?\d+),\s*(-?\d+))> velocity=<\s?(?:(-?\d+),\s*(-?\d+))>'
    for point in raw_points:
        match = re.match(regex, point)
        x, y, vx, vy = (int(coord) for coord in match.groups())
        points.append(Point(x, y, vx, vy))
    return points


def bounding_box(points: List[Point]) -> Tuple[Point, Point]:
    """
    Returns the smallest bounding box which contains all the points as a
    tuple with two points: the top left and bottom right.
    """
    min_x, min_y = (sys.maxsize, sys.maxsize)
    max_x, max_y = (-sys.maxsize, -sys.maxsize)

    for point in points:
        if point.x < min_x:
            min_x = point.x
        elif point.x > max_x:
            max_x = point.x
        if point.y < min_y:
            min_y = point.y
        elif point.y > max_y:
            max_y = point.y

    return (Point(min_x, min_y), Point(max_x, max_y))


def area(points: List[Point]) -> int:
    """
    Returns the size of the area formed by the points
    """
    top_left, bottom_right = bounding_box(points)
    return abs(bottom_right.x - top_left.x) * abs(bottom_right.y - top_left.y)


def render(points: List[Point]) -> None:
    """
    Visualizes the points by printing them to stdout
    """
    lights = set((point.x, point.y) for point in points)
    top_left, bottom_right = bounding_box(points)

    for y in range(top_left.y, bottom_right.y + 1):
        for x in range(top_left.x, bottom_right.x + 1):
            char = '*' if (x, y) in lights else '.'
            print(char, end='')
        print('\n', end='')


def find_message(points: List[Point]) -> int:
    """
    Returns the amount of seconds taken until the message is formed.

    As a side-effect after this function has been called the points
    will in the position where they form the message.
    """
    seconds = 0
    smallest_area = None
    found_message = False

    while not found_message:

        # Update points and compute
        for point in points:
            point.update()
        current_area = area(points)

        # Break when the area starts becoming larger
        if smallest_area is None or current_area <= smallest_area:
            smallest_area = current_area
        else:
            found_message = True
            break
        seconds += 1

    # Go backwards one iteration so that the points are in the position
    # where the area was the smallest, i.e. the time of the message
    for point in points:
        point.reverse()

    return seconds


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day10.in')) as f:
        points = parse(f.read().splitlines())

    seconds = find_message(points)
    print(f'Stopped after {seconds} seconds')
    assert seconds == 10391
    render(points)
