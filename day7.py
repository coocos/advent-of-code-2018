import re
import string
import os

from typing import List, Dict, Tuple
from enum import Enum


class State(Enum):
    """
    State of a single step
    """
    NOT_STARTED = 1
    STARTED = 2
    DONE = 3


class Step:
    """
    Represents a single step and contains references to the steps before it
    and after it.
    """
    def __init__(self,
                 name: str,
                 post: List['Step'],
                 pre: List['Step'],
                 state: State = State.NOT_STARTED) -> None:
        self.name = name
        self.post = post
        self.pre = pre
        self.state = state


def parse_steps(raw_steps: List[str]) -> List[Step]:
    """
    Parse steps from strings and return them as a list of Steps
    """
    regex = r'Step ([A-Z]) must be finished before step ([A-Z]) can begin'
    steps: Dict[str, Step] = {}

    # Create all steps and link them to each other
    for step in raw_steps:
        pre, post = re.match(regex, step).groups()
        if pre not in steps:
            steps[pre] = Step(pre, [], [])
        if post not in steps:
            steps[post] = Step(post, [], [])
        steps[pre].post.append(steps[post])
        steps[post].pre.append(steps[pre])

    return list(steps.values())


def find_next_steps(step) -> List[Step]:
    """
    Recursively finds all the steps which can be executed by following
    the starting step. Note that a better option would probably to treat
    the steps as an actual graph and do a topological sort.
    """
    # This step cannot be executed since a step before it has not finished
    if any(pre.state != State.DONE for pre in step.pre):
        return []

    if step.state == State.DONE:
        steps: List[Step] = []
    else:
        steps = [step]

    for next_step in step.post:
        steps += find_next_steps(next_step)

    return list(set(steps))


def execute_steps(steps: List[Step]) -> str:
    """
    Returns the execution order for the steps as a string
    """
    # A single root makes the algorithm easier to work with so
    # create a dummy root / step which precedes the first steps
    starting_steps = [step for step in steps if len(step.pre) == 0]
    entry_step = Step('_', starting_steps, [], state=State.DONE)
    next_steps = find_next_steps(entry_step)

    order = ''
    while next_steps:
        next_step = min(next_steps, key=lambda step: step.name)
        order += next_step.name
        next_step.state = State.DONE
        next_steps = find_next_steps(entry_step)
    return order


def execute_steps_in_parallel(steps: List[Step]) -> Tuple[str, int]:
    """
    Returns the execution order for the steps as a string
    """
    starting_steps = [step for step in steps if len(step.pre) == 0]
    entry_step = Step('_', starting_steps, [], State.DONE)
    next_steps = find_next_steps(entry_step)

    duration = {v: c + 61 for c, v in enumerate(string.ascii_uppercase)}
    workers = 5
    order = ''
    time = 0

    active_steps: Dict[Step, int] = {}

    while next_steps:

        # Mark progress on active steps and set them done if needed
        for step in list(active_steps.keys()):
            active_steps[step] -= 1
            if active_steps[step] == 0:
                step.state = State.DONE
                order += step.name
                del active_steps[step]

        next_steps = find_next_steps(entry_step)
        pending_steps = [step for step in next_steps if step.state == State.NOT_STARTED]

        if pending_steps:

            # Start any pending steps if there are workers available
            pending_steps.sort(key=lambda step: step.name, reverse=True)
            while len(active_steps) < workers and pending_steps:
                next_step = pending_steps.pop()
                next_step.state = State.STARTED
                active_steps[next_step] = duration[next_step.name]

        time += 1

    # Last second doesn't count since the steps were finished before it
    return order, time - 1


if __name__ == '__main__':

    with open(os.path.join('inputs', 'day7.in')) as f:
        raw_steps = f.read().splitlines()

    # Solve first part of the puzzle
    steps = parse_steps(raw_steps)
    assert execute_steps(steps) == 'GNJOCHKSWTFMXLYDZABIREPVUQ'

    # Solve second part of the puzzle
    steps = parse_steps(raw_steps)
    assert execute_steps_in_parallel(steps) == ('GNOYCHJWKXSTFZLAMBDIREPVUQ', 886)
