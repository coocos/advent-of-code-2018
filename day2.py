import os
from typing import Tuple, List
from collections import Counter


def generate_checksum_components(box: str) -> Tuple[int, int]:
    """
    Generates the checksum components from the string and returns a tuple
    indicating whether a character appeared twice or thrice in string. For
    example a (1, 1) would indicate that at least one character appeared twice
    and at least one character appeared thrice in the in the string.
    """
    character_count = Counter(box)

    twice = 0
    thrice = 0

    for count in character_count.values():
        if count == 2:
            twice = 1
        elif count == 3:
            thrice = 1
        if twice and thrice:
            break

    return (twice, thrice)


def find_common_name_for_boxes(boxes: List[str]) -> str:
    """
    A brute-force solution for finding two boxes where the difference in box
    names is limited to a single character. Returns the common characters in
    the box names.

    The algorithm just loops through the boxes and compares the box name
    against all of the boxes after it. If the compared box names differ only by
    1 then we've found the boxes we're looking for.  Since the input is small
    this brute-force O(n^2) solution is fast enough.
    """
    for i, box_1 in enumerate(boxes):
        for box_2 in boxes[i + 1:]:
            differ = 0
            for character_1, character_2 in zip(box_1, box_2):
                if character_1 != character_2:
                    differ += 1
            if differ == 1:
                return ''.join(a for a, b in zip(box_1, box_2) if a == b)
    return ''


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day2.in')) as f:
        boxes = f.read().splitlines()

    # Generate checksum for the first half of the puzzle
    total_twice = 0
    total_thrice = 0
    for box in boxes:
        twice, thrice = generate_checksum_components(box)
        total_twice += twice
        total_thrice += thrice
    assert total_twice * total_thrice == 4920

    # Find the prototype box for the second half of the puzzle
    common_name = find_common_name_for_boxes(boxes)
    assert common_name == 'fonbwmjquwtapeyzikghtvdxl'
