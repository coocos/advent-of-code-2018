from collections import defaultdict
from typing import DefaultDict


def play(player_count: int, last_marble: int) -> int:
    """
    An awfully inefficient solution to the marble problem. What
    makes this solution bad is the fact that Python lists do not
    provide O(1) insertions or removals so this solution should
    really be rewritten using a data structure which does, e.g
    a custom linked list or perhaps collections.deque.
    """
    position = 0
    scores: DefaultDict[int, int] = defaultdict(int)
    board = [0]

    for marble in range(1, last_marble + 1):

        if marble % 23 != 0:
            if len(board) > 1:
                position = (position + 2)
                if position > len(board):
                    position = position % len(board)
            else:
                position = 1

            board.insert(position, marble)
        else:
            scores[marble % player_count] += marble
            position = (position - 7) % len(board)
            scores[marble % player_count] += board[position]
            del board[position]

    return max(scores.values())


if __name__ == '__main__':

    assert play(9, 25) == 32
    assert play(10, 1618) == 8317
    assert play(13, 7999) == 146373
    assert play(17, 1104) == 2764
    assert play(21, 6111) == 54718
    assert play(30, 5807) == 37305
    assert play(427, 70723) == 399745
    assert play(427, 70723 * 100) == 3349098263
