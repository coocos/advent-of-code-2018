from typing import Optional


class Node:
    """
    Simple linked list with append and move operations
    """
    def __init__(self, value: int) -> None:
        self.value = value
        self.next: Optional['Node'] = None

    def append(self, node: 'Node') -> 'Node':
        """
        Appends to the end of the linked list
        """
        head = self
        while head.next:
            head = head.next
        head.next = node
        return head.next

    def move(self, root: 'Node') -> 'Node':
        """
        Returns the node value + 1 steps further in the linked list.

        If the end of the linked list is reached before value + 1 steps then
        the head is set to the passed node and the iteration continues until
        value + 1 steps are reached.
        """
        node = self
        for _ in range(1 + self.value):
            node = node.next
            if node is None:
                node = root
        return node


def first_half(root: Node, offset: int, n: int) -> str:
    """
    This solution constructs a circular linked list of recipes up to input + n
    recipes according to the recipe construction rules. Once the linked list
    has been constructed it is traversed to the input'th recipe and the rest of
    the recipes are returned as a combined string.
    """
    first = root
    second = root.next
    last = second

    recipes = 2  # Amount of recipes

    while recipes <= offset + n:

        # Add next recipes to the list
        next_recipes = first.value + second.value
        first_recipe, second_recipe = (next_recipes // 10, next_recipes % 10)
        if first_recipe:
            last = last.append(Node(first_recipe))
            recipes += 1
        last = last.append(Node(second_recipe))
        recipes += 1

        # Move elves to the next recipes
        first = first.move(root)
        second = second.move(root)

    # Traverse until the recipe offset point is reached
    head = root
    for _ in range(offset):
        head = head.next

    # Construct string with n recipes after the recipe offset point
    scores = ''
    for _ in range(n):
        scores += str(head.value)
        head = head.next
    return scores


def second_half(root: Node, sequence: str) -> int:
    """
    This solution is similar to the first half but instead it keeps
    constructing the linked list until the last n recipes match the target
    sequence recipes. At that point the number of recipes before the sequence
    started is returned.

    This solution is fairly ugly and not that great performance-wise, oh well.
    """
    first = root
    second = root.next
    last = second

    recipes = 2  # Amount of recipes
    matches = 0  # How many recipes in the sequence we've matched
    target = [int(c) for c in sequence]

    while True:

        # Construct next recipes
        next_recipes = first.value + second.value
        first_recipe, second_recipe = (next_recipes // 10, next_recipes % 10)

        try:
            if first_recipe:
                last = last.append(Node(first_recipe))
                recipes += 1
                if first_recipe == target[matches]:
                    matches += 1
                else:
                    matches = 0
            last = last.append(Node(second_recipe))
            recipes += 1

            if second_recipe == target[matches]:
                matches += 1
            else:
                matches = 0
            if matches == 0 and second_recipe == target[matches]:
                matches += 1

        # We've matched target sequence so we're done
        except IndexError:
            return recipes - len(sequence) - 1

        # Move elves to the next recipes
        first = first.move(root)
        second = second.move(root)


if __name__ == '__main__':

    # Solve first half the puzzle
    root = Node(3)
    root.next = Node(7)
    assert first_half(root, 909441, 10) == '2615161213'

    # Solve second half of the puzzle
    root = Node(3)
    root.next = Node(7)
    assert second_half(root, '909441') == 20403320
