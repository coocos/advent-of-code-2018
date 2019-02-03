from typing import List
from collections import namedtuple


"""
Simple data container for nodes. Children is a list of child nodes, tokens
holds the license tokens for this node, i.e. the header, children and the
metadata. Entries contains just the metadata entries for this node.
"""
Node = namedtuple('Node', 'children, tokens, entries')


def recursive(license: List[int]) -> Node:
    """
    Constructs a tree from the license.

    The algorithm recursively parses the license until a terminal node is
    reached. Then the terminal node is returned and the parent node subtracts
    the child node tokens from the license to determine where its metadata
    entries start at.
    """
    child_count, meta = license[:2]

    if child_count == 0:
        return Node([], license[:2 + meta], license[2:2 + meta])
    else:
        children = []
        child_tokens: List[int] = []  # License tokens for children of the node

        # Construct child nodes
        for child in range(child_count):
            node = recursive(license[2 + len(child_tokens):])
            child_tokens += node.tokens
            children.append(node)

        tokens = license[:2] + child_tokens
        # Metadata starts after all the child license tokens
        entries = license[len(tokens): len(tokens) + meta]

        return Node(children, tokens + entries, entries)


def all_entries(node: Node) -> List[int]:
    """
    Returns all metadata entries from the license
    """
    if not node.children:
        return node.entries
    else:
        child_entries: List[int] = []
        for child in node.children:
            child_entries += all_entries(child)
        return node.entries + child_entries


def node_value(node: Node) -> int:
    """
    Computes the value of node
    """
    if not node.children:
        return sum(node.entries)
    else:
        value = 0
        for entry in node.entries:
            try:
                # Entries start at 1 so subtract all entries by 1
                value += node_value(node.children[entry - 1])
            except IndexError:
                pass
        return value


if __name__ == '__main__':

    simple_license = '2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2'
    license_tokens = [int(token) for token in simple_license.split(' ')]
    node = recursive(license_tokens)
    assert sum(all_entries(node)) == 138
    assert node_value(node) == 66

    with open('day8.in') as f:
        complex_license = f.read()

    license_tokens = [int(token) for token in complex_license.split(' ')]
    node = recursive(license_tokens)
    assert sum(all_entries(node)) == 44838
    assert node_value(node) == 22198
