import os

from collections import namedtuple, deque
from typing import List, Tuple, Iterable


Vec = namedtuple('Vec', 'x, y')
Cave = List[List[str]]
neighbours = (Vec(-1, 0), Vec(0, -1), Vec(1, 0), Vec(0, 1))


def surrounding(pos: Vec) -> Iterable[Vec]:
    """
    Returns the positions surrounding the passed position, i.e. the vectors
    left, above, right and bottom of the passed position.
    """
    return (Vec(pos.x + n.x, pos.y + n.y) for n in neighbours)


class Unit:
    """An individual elf or goblin"""
    def __init__(self, pos: Vec, race: str = 'E') -> None:
        self.pos = pos
        self.hp = 200
        self.race = race
        self.cave: Cave = []
        self.others: List[Unit] = []  # Other elves and goblins
        self.attack_power = 3
        self.alive = True

    @property
    def reachable(self) -> bool:
        """Indicates if unit has at least one empty square around it"""
        unit_positions = set(unit.pos for unit in self.others if unit.alive)
        for pos in surrounding(self.pos):
            square = self.cave[pos.y][pos.x]
            if square == '.' and pos not in unit_positions:
                return True
        return False

    def should_attack(self) -> bool:
        """
        Indicates if the unit should attack because it's surrounded by at least
        one enemy unit.
        """
        enemies = set(o.pos for o in self.others if o.race != self.race and o.alive)
        for pos in surrounding(self.pos):
            if pos in enemies:
                return True
        return False

    def attack(self) -> None:
        """
        Attacks a surrounding enemy chosen according to the attack rules, i.e.
        the enemy with the lowest hit points. Ties are broken by reading order.
        """
        # Find all enemies which surround this unit
        enemies = [o for o in self.others if o.race != self.race and o.alive]
        enemies_to_attack = []
        for pos in surrounding(self.pos):
            for enemy in enemies:
                if enemy.pos == pos:
                    enemies_to_attack.append(enemy)

        # Sort by hit points and break ties by reading order to find the target
        enemies_to_attack.sort(key=lambda e: (e.pos.y, e.pos.x))
        enemies_to_attack.sort(key=lambda e: e.hp)
        enemy = enemies_to_attack[0]

        enemy.hp -= self.attack_power
        if enemy.hp <= 0:
            enemy.alive = False

    def __repr__(self):
        return f'{self.race} {self.hp} hp @ {self.pos}'


def draw(cave: Cave, units: List[Unit]) -> None:
    """Debug routine for drawing the cave and units"""
    unit_positions = {unit.pos: unit for unit in units if unit.alive}

    for y, row in enumerate(cave):
        units_in_row = []
        for x, col in enumerate(row):
            unit = unit_positions.get(Vec(x, y))
            if unit:
                print(unit.race, end='')
                units_in_row.append(unit)
            else:
                print(col, end='')
        hps = [f'{unit.race}({unit.hp})' for unit in units_in_row]
        print('  ', ', '.join(hps))


def parse_input(input_: List[str]) -> Tuple[Cave, List[Unit]]:
    """
    Parses the input and creates the cave and units
    """
    cave: Cave = []
    units: List[Unit] = []

    for y, row in enumerate(input_):
        cols: List[str] = []
        for x, col in enumerate(row):
            if col in ('E', 'G'):
                units.append(Unit(Vec(x, y), col))
                cols.append('.')
            else:
                cols.append(col)
        cave.append(cols)

    for unit in units:
        unit.cave = cave
        unit.others = [other for other in units if other != unit]

    return cave, units


def battle(units: List[Unit], cave: Cave) -> bool:
    """
    Performs one iteration of battle and returns True if the battle ended
    during the iteration and False if not.
    """
    # Order the units according to reading order before moving
    ordered = sorted(units, key=lambda unit: (unit.pos.y, unit.pos.x))

    for unit in ordered:

        # Only elves or goblins left, battle is over
        if len(set(u.race for u in units if u.alive)) != 2:
            return True
        if not unit.alive:
            continue
        if unit.should_attack():
            unit.attack()
            continue

        # Find squares in range of enemies, i.e. the surrounding squares
        squares_in_range = set()
        enemies = set(o.pos for o in unit.others if o.reachable and o.race != unit.race and o.alive)
        for e in enemies:
            # Gather empty surrounding squares around the enemies
            for pos in surrounding(e):
                if cave[pos.y][pos.x] == '.' and pos not in enemies:
                    squares_in_range.add(pos)

        # Find reachable squares in range of enemies with breadth-first search
        queue = deque([unit.pos])
        visited = {unit.pos}
        distances = {unit.pos: 0}
        unit_positions = set(u.pos for u in units if u.alive)
        while queue:
            s = queue.popleft()
            for pos in surrounding(s):
                if cave[pos.y][pos.x] == '.' and pos not in unit_positions and pos not in visited:
                    queue.append(pos)
                    visited.add(pos)
                    distances[pos] = distances[s] + 1
        reachable = visited & squares_in_range

        # Unit cannot reach any of its target squares so skip to the next unit
        if not reachable:
            continue

        # Find the nearest reachable square in reading order
        nearest = [(pos.x, pos.y, distances[pos]) for pos in reachable]
        nearest.sort(key=lambda xyd: (xyd[1], xyd[0]))
        nearest.sort(key=lambda xyd: xyd[2])
        chosen = Vec(nearest[0][0], nearest[0][1])

        # Search for the shortest path to the chosen square
        queue = deque([chosen])
        visited = {chosen}
        distances = {chosen: 0}
        while queue:
            s = queue.popleft()
            for pos in surrounding(s):
                if cave[pos.y][pos.x] == '.' and \
                   pos not in unit_positions and \
                   pos not in visited:
                    queue.append(pos)
                    visited.add(pos)
                    distances[pos] = distances[s] + 1

        # Generate all movements and their distance to the chosen square
        movements = []
        for pos in surrounding(unit.pos):
            if cave[pos.y][pos.x] == '.' and pos not in unit_positions:
                try:
                    movements.append((pos.x, pos.y, distances[pos]))
                except KeyError:
                    # Position has no distance because it's not reachable
                    pass

        # Find the movement which gives us the shortest path to chosen square
        movements.sort(key=lambda xyd: (xyd[1], xyd[0]))
        movements.sort(key=lambda xyd: xyd[2])
        movement = Vec(movements[0][0], movements[0][1])
        unit.pos = movement

        # Unit has reached an enemy after moving and needs to attack
        if unit.should_attack():
            unit.attack()

    return False


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day15.in')) as f:
        description = f.read().splitlines()

    """
    Solve the first half of the puzzle by simply executing the battle.
    """
    cave, units = parse_input(description)
    draw(cave, units)

    iteration = 0
    while len(set(u.race for u in units if u.alive)) == 2:
        done = battle(units, cave)
        if not done:
            iteration += 1

    hps = sum(u.hp for u in units if u.alive)
    print(f'Combat ends after {iteration} full rounds')
    print(f'Winner has {hps} total hit points  left')
    print(f'Outcome: {iteration} * {hps} = {iteration * hps}')
    assert iteration * hps == 197025

    """
    Just apply brute force for the second-part and use a linear search
    for the lowest attack power boost which guarantees the elves win
    without casualties. A binary search would obviously be faster but
    a linear approach works just fine as well.
    """
    for attack_power in range(4, 1000000):

        cave, units = parse_input(description)

        # Boost the elven attack power
        elves = [unit for unit in units if unit.race == 'E']
        for elf in elves:
            elf.attack_power = attack_power

        iteration = 0
        while len(set(u.race for u in units if u.alive)) == 2:
            done = battle(units, cave)
            if not done:
                iteration += 1

        hps = sum(u.hp for u in units if u.alive)
        print(f'Combat ends after {iteration} full rounds')
        print(f'Winner has {hps} total hit points  left')
        print(f'Outcome: {iteration} * {hps} = {iteration * hps}')
        print(f'Attack power: {attack_power}')

        if all(elf.alive for elf in elves):
            print('All elves are alive, yay!')
            break

    assert attack_power == 23
    assert iteration * hps == 44423
