import re
from copy import deepcopy
from typing import List, Tuple, Set, Optional


class Group:
    """
    A group engaged in the epic battle for the fate of the precious reindeer.
    """
    def __init__(self,
                 name: str,
                 units: int,
                 hp: int,
                 weaknesses: Set[str],
                 immunities: Set[str],
                 damage: int,
                 attack_type: str,
                 initiative: int) -> None:
        self.name = name
        self.units = units
        self.hp = hp
        self.weaknesses = weaknesses
        self.immunities = immunities
        self.damage = damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.target: Optional['Group'] = None

    def damage_dealt(self, enemy: 'Group') -> int:
        """
        How much damage this group would deal to the enemy when immunities and
        weaknesses are taken into account.
        """
        multiplier = int(self.attack_type in enemy.weaknesses) + 1
        multiplier *= int(self.attack_type not in enemy.immunities)
        return multiplier * self.effective_power

    @property
    def effective_power(self):
        """Effective power of the group, i.e. units times damage"""
        return self.units * self.damage


def parse_army(definitions: List[str], type_: str) -> List[Group]:
    """
    Parses the army definition and returns the army as a list of Groups.
    """
    groups = []

    # The regex pattern is unfortunately too long for PEP-8
    pattern = ('(\d+) units each with (\d+) '
               'hit points (?:\(([a-z,-; ]+)\) )?'
               'with an attack that does (\d+) ([a-z]+) '
               'damage at initiative (\d+)')

    for number, definition in enumerate(definitions):

        match = re.match(pattern, definition)

        units = int(match.group(1))
        hp = int(match.group(2))
        damage = int(match.group(4))
        attack = match.group(5)
        initiative = int(match.group(6))
        name = f'{type_}-{number + 1}'

        """
        Parsing the immunities and weaknesses is a bit awkward in the main
        regex as their order can vary among other things so parse them
        separately here based on the initial regex group
        """
        weaknesses: Set[str] = set()
        immunities: Set[str] = set()
        defense = match.group(3)
        if defense:
            w = re.search(r'weak to ([a-z, ]+)', defense)
            i = re.search(r'immune to ([a-z, ]+)', defense)
            if w is not None:
                weaknesses = set(w.strip() for w in w.group(1).split(','))
            if i is not None:
                immunities = set(i.strip() for i in i.group(1).split(','))

        groups.append(Group(name,
                            units,
                            hp,
                            weaknesses,
                            immunities,
                            damage,
                            attack,
                            initiative))

    return groups


def battle(immune: List[Group], infection: List[Group]) -> Tuple[int, str]:
    """
    Wage battle between the armies and return how many units are left after
    the battle and which army won.
    """
    groups = immune + infection

    while True:

        # Remove groups which have perished
        groups = [group for group in groups if group.units > 0]
        immune = [group for group in immune if group.units > 0]
        infection = [group for group in infection if group.units > 0]

        # If one of the armies has completely perished then we're done
        if not immune or not infection:
            winner = 'immune' if immune else 'infection'
            return sum(group.units for group in groups), winner

        # Sort for selection phase by effective power and break ties by
        # relying on stable sorting by secondary criteria
        groups.sort(key=lambda g: g.initiative, reverse=True)
        groups.sort(key=lambda g: g.effective_power, reverse=True)
        groups.sort(key=lambda g: g.name[:2], reverse=True)

        targeted: Set[str] = set()  # Groups which have already been targeted

        for group in groups:

            enemies = infection if group.name.startswith('immune') else immune

            # Calculate the damage for all the targets this group can attack
            targets = []
            for enemy in enemies:
                if enemy.name not in targeted:
                    damage = group.damage_dealt(enemy)
                    if damage > 0:
                        targets.append((enemy, damage))

            if targets:

                # Find best target by relying on stable sorting to break ties
                targets.sort(key=lambda t: t[0].initiative, reverse=True)
                targets.sort(key=lambda t: t[0].effective_power, reverse=True)
                targets.sort(key=lambda t: t[1], reverse=True)
                enemy, damage = targets[0]

                targeted.add(enemy.name)
                group.target = enemy

        # Group with highest initiative charges first
        groups.sort(key=lambda g: g.initiative, reverse=True)

        casualties = 0
        for group in groups:
            if group.target and group.units > 0:
                damage = group.damage_dealt(group.target)
                kills = damage // group.target.hp
                group.target.units -= kills
                casualties += kills
                group.target = None

        # A tie can occur if neither army is able to kill any units
        if not casualties:
            return sum(group.units for group in groups), 'neither'


if __name__ == '__main__':

    with open('day24.in') as f:
        lines = f.read().splitlines()

    immune = parse_army(lines[1:lines.index('')], 'immune')
    infection = parse_army(lines[lines.index('') + 2:], 'infection')

    # First part of the puzzle - just wage war
    units_left, winner = battle(deepcopy(immune), deepcopy(infection))
    assert units_left, winner == (20150, 'infection')

    """
    Second part of the puzzle. Apply boost and find the tipping point where
    the immune system overcomes the infection. You could do a binary search
    here as well but linear iteration finds the solution for at least this
    particular input reasonably fast.
    """
    for boost in range(1, 1000):
        boosted_immune = deepcopy(immune)
        boosted_infection = deepcopy(infection)
        for immune_group in boosted_immune:
            immune_group.damage += boost
        units_left, winner = battle(boosted_immune, boosted_infection)
        if winner == 'immune':
            break
    assert units_left == 13005
