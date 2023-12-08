import os
from itertools import islice
from collections import Counter
from math import lcm


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def keep_iterating(data):
    while True:
        for thing in data:
            yield thing


def transform(lines):
    it = iter(lines)
    route = next(it)
    links = {}
    for line in it:
        if "=" not in line:
            continue
        node, bits = line.split(" = ")
        links[node] = bits[1:-1].split(", ")
    return route, links


def calculate_part_1(test=False):
    lines = read(1, test=test)
    route, links = transform(lines)
    location = "AAA"
    it = enumerate(keep_iterating(route), 1)
    while location != "ZZZ":
        choice_num, choice = next(it)
        location = links[location][1 if choice == "R" else 0]
    return choice_num


def calculate_part_2_brute_force(test=False):
    lines = read(2, test=test)
    route, links = transform(lines)
    locations = [k for k in links if k.endswith("A")]
    it = enumerate(keep_iterating(route), 1)
    choice_num = None
    lowest, lowest_num = len(locations), 0
    while True:
        choice_num, choice = next(it)
        locations = [links[l][1] if choice == "R" else links[l][0] for l in locations]
        num_left = len([l for l in locations if not l.endswith("Z")])
        if num_left < lowest:
            lowest, lowest_num = num_left, choice_num
        if choice_num % 500000 == 0:
            print(f"Iteration {choice_num}: best was {lowest}, on #{lowest_num}")
        if num_left == 0:
            break
    return choice_num


def calculate_part_2(test=False):
    lines = read(2, test=test)
    route, links = transform(lines)
    starts = [n for n in links if n.endswith("A")]
    periodicities = {s: periodicity(route, links, s) for s in starts}
    result = lcm(*periodicities.values())
    return result


def count_visits(route, links, start, iterations=1000000):
    counter = Counter()
    location = start
    for choice in islice(keep_iterating(route), iterations):
        options = links[location]
        location = options[1 if choice == "R" else 0]
        counter.update([location])
    return counter


def initial_tyre_kicking():
    lines = read(2, test=False)
    route, links = transform(lines)
    starts = [n for n in links if n.endswith("A")]
    for start in starts:
        counts = count_visits(route, links, start)
        print(counts)


def count_gaps(route, links, start, iterations=200000):
    destinations = {}
    location = start
    for idx, choice in islice(enumerate(keep_iterating(route), 1), iterations):
        options = links[location]
        location = options[1 if choice == "R" else 0]
        if location.endswith("Z"):
            if location in destinations:
                destinations[location].append(idx)
            else:
                destinations[location] = [idx]
    return destinations


def do_some_exploration():
    lines = read(2, test=False)
    route, links = transform(lines)
    starts = [n for n in links if n.endswith("A")]
    for start in starts:
        destinations = count_gaps(route, links, start)
        print(f"Starting from {start}, destinations are: ")
        print(destinations)
        nums = list(destinations.values())[0]
        gaps = [num - prev_num for num, prev_num in zip(nums, [0] + nums)]
        print(gaps)


def periodicity(route, links, start):
    destinations = count_gaps(route, links, start)
    results = list(destinations.items())
    assert len(results) == 1
    nums = list(results[0][1])
    gaps = Counter([n - p for n, p in zip(nums, [0] + nums)])
    assert len(gaps) == 1
    return gaps.most_common()[0][0]


for part, function, test_result in [
    (1, calculate_part_1, 6),
    (2, calculate_part_2, 6),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
