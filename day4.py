import re
import os
from datetime import datetime, timedelta
from collections import namedtuple, defaultdict, Counter
from typing import List, Dict, Tuple


Record = namedtuple('Record', 'time, event')


def parse_records(raw_records: List[str]) -> List[Record]:
    """
    Parses list of string records to Records
    """
    TIMESTAMP_FORMAT = r'%Y-%m-%d %H:%M'
    RECORD_REGEX = r'\[(.*)\] (.*)'

    records = []
    for record in raw_records:
        match = re.match(RECORD_REGEX, record)
        time = datetime.strptime(match.group(1), TIMESTAMP_FORMAT)
        records.append(Record(time, match.group(2)))
    return records


def sleepiest_guard(records: List[Record], strategy: int) -> Tuple[int, int]:
    """
    Finds the sleepiest guard according to either the first or second strategy
    and returns the guard identifier and the minute they slept most on.
    """
    # Map from guard to how long they slept in total
    total_slept: Dict[int, timedelta] = defaultdict(timedelta)
    # Map from guard to which minutes they slept on
    minutes_slept: Dict[int, List] = defaultdict(list)

    start = None

    # Collect guard sleep times to a dictionary
    for record in records:
        if record.event.startswith('Guard'):
            guard = int(re.match('Guard #(\d+)', record.event).group(1))
        elif record.event.startswith('falls'):
            start = record.time
        else:
            total_slept[guard] += record.time - start
            minutes_slept[guard] += list(range(start.minute, record.time.minute))

    # Find the guard who slept the most and their most slept minute
    if strategy == 1:
        worst_guard, _ = max(total_slept.items(), key=lambda slept: slept[1])
        laziest_minute, _ = Counter(minutes_slept[worst_guard]).most_common(1)[0]
        return (worst_guard, laziest_minute)
    # Find the guard who slept most during a single minute
    else:
        laziest_minute = 0
        most_slept = 0
        worst_guard = -1
        for guard, minutes in minutes_slept.items():
            most_slept_minute, count = Counter(minutes).most_common(1)[0]
            if count > most_slept:
                worst_guard = guard
                laziest_minute = most_slept_minute
                most_slept = count
        return (worst_guard, laziest_minute)


if __name__ == '__main__':

    example_data = [
        '[1518-11-01 00:00] Guard #10 begins shift',
        '[1518-11-01 00:05] falls asleep',
        '[1518-11-01 00:25] wakes up',
        '[1518-11-01 00:30] falls asleep',
        '[1518-11-01 00:55] wakes up',
        '[1518-11-01 23:58] Guard #99 begins shift',
        '[1518-11-02 00:40] falls asleep',
        '[1518-11-02 00:50] wakes up',
        '[1518-11-03 00:05] Guard #10 begins shift',
        '[1518-11-03 00:24] falls asleep',
        '[1518-11-03 00:29] wakes up',
        '[1518-11-04 00:02] Guard #99 begins shift',
        '[1518-11-04 00:36] falls asleep',
        '[1518-11-04 00:46] wakes up',
        '[1518-11-05 00:03] Guard #99 begins shift',
        '[1518-11-05 00:45] falls asleep',
        '[1518-11-05 00:55] wakes up'
    ]
    records = sorted(parse_records(example_data), key=lambda rec: rec.time)
    assert sleepiest_guard(records, strategy=1) == (10, 24)
    assert sleepiest_guard(records, strategy=2) == (99, 45)

    with open(os.path.join('inputs', 'day4.in')) as f:
        complex_data = f.read().splitlines()

    records = sorted(parse_records(complex_data), key=lambda rec: rec.time)
    assert sleepiest_guard(records, strategy=1) == (2851, 44)
    assert sleepiest_guard(records, strategy=2) == (733, 25)
