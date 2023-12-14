import os
from collections import Counter
from itertools import islice
import hashlib


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def get_column(lines, col):
    return "".join(l[col] for l in lines)


def transpose(lines):
    return ["".join(l[c] for l in lines) for c, _ in enumerate(lines[0])]


def tilt(column, to_top=True):
    return "#".join("".join(sorted(c, reverse=to_top)) for c in column.split("#"))


def tilt_lines(lines, direction):
    need_transpose = direction in "NS"
    to_top = direction in "NW"
    stacks = transpose(lines) if need_transpose else lines
    tilted = [tilt(s, to_top) for s in stacks]
    return transpose(tilted) if need_transpose else tilted


def fingerprint(lines):
    m = hashlib.sha256()
    for l in lines:
        m.update(l.encode("utf8"))
    return m.hexdigest()


def weigh(stack):
    return sum(d for d, s in enumerate(stack[::-1], 1) if s == "O")


def weigh_lines(lines):
    total = 0
    for n, l in enumerate(lines[::-1], 1):
        total += n * sum(1 for c in l if c == "O")
    return total


def cycle_lines(lines):
    for d in "NWSE":
        lines = tilt_lines(lines, d)
    return lines


def project_weight(lines, num_cycles, warm_up=199, capture_num=1000):
    assert num_cycles > warm_up, "For small numbers, just work it out"
    cycle_count = iter(range(1, 1000000000))

    print(f"Phase 1: stabilise with {warm_up} iterations")
    for _ in islice(cycle_count, warm_up):
        lines = cycle_lines(lines)

    print(f"Phase 2: run {capture_num} more cycles for forecasting")
    captured = []
    for cycle_no in islice(cycle_count, capture_num):
        lines = cycle_lines(lines)
        captured.append((cycle_no, fingerprint(lines), weigh_lines(lines)))

    print("Checking forecasting is going to work")
    fingerprints = Counter(f for _, f, _ in captured)
    counts = Counter(f for _, f in fingerprints.items())
    assert len(counts) in (1, 2), "No obvious pattern"

    print("Working out the periodicity")
    to_find = tuple(c[1] for c in captured[:3])
    found_at = [
        i
        for i in range(1, len(captured) - 2)
        if tuple(c[1] for c in captured[i : i + 3]) == to_find
    ]
    periodicity = found_at[0]
    outcome_index = (num_cycles - captured[0][0]) % periodicity
    print(f"Target {num_cycles} should land at offset {outcome_index}")
    return captured[outcome_index][2]


def calculate_part_1(test=False):
    lines = read(1, test=test)
    columns = (get_column(lines, c) for c, _ in enumerate(lines[0]))
    tilted = map(tilt, columns)
    return sum(map(weigh, tilted))


def calculate_part_2(test=False):
    lines = read(1, test=test)
    return project_weight(lines, 1_000_000_000)


for part, function, test_result in [
    (1, calculate_part_1, 136),
    (2, calculate_part_2, 64),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
