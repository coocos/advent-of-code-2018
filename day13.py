from typing import List, Dict
from collections import namedtuple, deque


Vec = namedtuple('Vec', 'x, y')


class Cart:
    """
    Represents a single cart using a position vector and a direction vector
    """
    def __init__(self, pos: Vec, dir_: Vec) -> None:
        self.pos = pos
        self.dir = dir_
        self.crashed = False
        """
        A fixed-size deque makes it trivial to keep track of which direction
        the cart will turn at the next intersection as you can simply call
        deque.rotate(-1) whenever an intersection is encountered and it will
        rotate to the next direction.
        """
        self.next_intersection = deque(('left', 'straight', 'right'))

    def update(self, segment: str):
        """
        Updates the cart to its next position according to the part of track
        it is on. Direction is also updated accordingly.
        """
        if not self.crashed:
            if segment == '/':
                self.dir = Vec(-self.dir.y, -self.dir.x)
            elif segment == '\\':
                self.dir = Vec(self.dir.y, self.dir.x)
            elif segment == '+':
                if self.next_intersection[0] == 'left':
                    if self.dir.y == 0:
                        self.dir = Vec(0, -self.dir.x)
                    else:
                        self.dir = Vec(self.dir.y, 0)
                elif self.next_intersection[0] == 'right':
                    if self.dir.y == 0:
                        self.dir = Vec(0, self.dir.x)
                    else:
                        self.dir = Vec(-self.dir.y, 0)
                elif self.next_intersection[0] == 'straight':
                    pass
                self.next_intersection.rotate(-1)
            self.pos = Vec(self.pos.x + self.dir.x, self.pos.y + self.dir.y)


def create_track(track_rows: List[str]) -> List[List[str]]:
    """
    Parses the track and returns it as a graph / list of lists. Cart markers
    are ignored and replaced with correct track segments.
    """
    track: List[List[str]] = []

    for y in range(len(track_rows)):
        segments = []
        for segment in track_rows[y]:
            if segment == '^':
                segment = '|'
            elif segment == '>':
                segment = '-'
            elif segment == '<':
                segment = '-'
            elif segment == 'v':
                segment = '|'
            segments.append(segment)
        track.append(segments)
    return track


def create_carts(track_rows: List[str]) -> List[Cart]:
    """
    Parses the track and returns a list of Carts.
    """
    carts: List[Cart] = []

    for y in range(len(track_rows)):
        for x, segment in enumerate(track_rows[y]):
            if segment in ('^', 'v', '<', '>'):
                if segment == '^':
                    direction = Vec(0, -1)
                elif segment == '>':
                    direction = Vec(1, 0)
                elif segment == '<':
                    direction = Vec(-1, 0)
                else:
                    direction = Vec(0, 1)
                position = Vec(x, y)
                carts.append(Cart(position, direction))

    return carts


def find_crashes(carts: List[Cart]) -> List[Vec]:
    """
    Checks carts for crashes and returns coordinates for any crashes. As a
    side-effect if a cart is found to have crashed it is flagged as crashed.
    """
    cart_at: Dict[Vec, Cart] = {}
    crashes: List[Vec] = []

    for cart in carts:
        if not cart.crashed:
            if cart.pos in cart_at:
                crashes.append(cart.pos)
                cart.crashed = True
                cart_at[cart.pos].crashed = True
            else:
                cart_at[cart.pos] = cart
    return crashes


if __name__ == '__main__':

    """
    The first half of the puzzle can be solved by constructing a graph of the
    track and then running a simulation of the carts on the graph.
    """
    with open('day13.in') as f:
        original_track = f.read().splitlines()
        carts = create_carts(original_track)

    crashes: List[Vec] = []
    while not crashes:
        for cart in sorted(carts, key=lambda cart: cart.pos):
            cart.update(original_track[cart.pos.y][cart.pos.x])
            crashes = find_crashes(carts)
            if crashes:
                break

    assert crashes[0] == Vec(116, 10)

    """
    The second half of the puzzle is essentially the same thing but the exit
    condition is that only one cart is left so loop until only one cart is
    left.
    """
    carts = create_carts(original_track)

    crashes = []
    while len([cart for cart in carts if not cart.crashed]) > 1:
        for cart in sorted(carts, key=lambda cart: cart.pos):
            cart.update(original_track[cart.pos.y][cart.pos.x])
            _ = find_crashes(carts)

    # Get the last cart still riding around
    cart = [cart for cart in carts if not cart.crashed][0]
    assert cart.pos == Vec(116, 25)
