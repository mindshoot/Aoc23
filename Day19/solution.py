import os
from functools import reduce
import operator


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


X, M, A, S = 0, 1, 2, 3
INDEXES = {"x": X, "m": M, "a": A, "s": S}
ACCEPT, REJECT = "A", "R"


def parse_rule(line):
    key, parts = line.split("{")
    rules = []
    for clause in parts[:-1].split(","):
        if ":" in clause:
            rule, outcome = clause.split(":")
            rules.append((INDEXES[rule[0]], rule[1], int(rule[2:]), outcome))
        else:
            rules.append((None, None, None, clause))
    return key, rules


def parse_rules(lines):
    return dict(parse_rule(line) for line in lines)


def parse_rating(line):
    parts = line[1:-1].split(",")
    d = {p[0]: int(p[2:]) for p in parts}
    return [d[k] for k in ("x", "m", "a", "s")]


def parse_ratings(lines):
    return list(map(parse_rating, lines))


def get_range(ratings):
    cols = [[r[c] for r in ratings] for c in range(4)]
    return [[min(col), max(col)] for col in cols]


def partition_space(range, rules):
    spaces = [(range, "?")]
    queue = [(0, "in", 0)]

    while len(queue) > 0:
        (index, key, ofs), queue = queue[0], queue[1:]
        rng, state = spaces[index]
        if key in {ACCEPT, REJECT}:
            spaces[index] = (rng, key)
            continue
        assert state == "?", "Should not be processing spaces that are already known"
        field, condition, value, outcome = rules[key][ofs]
        if field is None:
            queue.append((index, outcome, 0))
            continue
        rmin, rmax = rng[field]
        assert rmin <= rmax, "Range order broken"
        # Three scenarios: none, some or all of the range meets the criterion
        if (condition == ">" and rmin > value) or (condition == "<" and rmax < value):
            this_result = True
            new_idx = None
        elif (condition == ">" and rmax <= value) or (
            condition == "<" and rmin >= value
        ):
            this_result = False
            new_idx = None
        else:
            # Need to split this space, continue on one side and add the other to the queue
            new_idx = len(spaces)
            new_rng = [c[:] for c in rng]
            if condition == ">":
                new_rng[field][0] = value + 1
                rng[field][1] = value
                this_result = False
            else:
                new_rng[field][0] = value
                rng[field][1] = value - 1
                this_result = True
            spaces.append((new_rng, "?"))

        # Process the range that meets the condition
        if this_result == True or (this_result == False and new_idx is not None):
            i = index if this_result else new_idx
            queue.append((i, outcome, 0))
        # Process the range that doesn't meet the condition
        if this_result == False or (this_result == True and new_idx is not None):
            i = new_idx if this_result else index
            new_key, new_ofs = (
                (key, ofs + 1) if ofs + 1 < len(rules[key]) else (outcome, 0)
            )
            queue.append((i, new_key, new_ofs))

    return spaces


def calc_score(ratings, spaces):
    score = 0
    for point in ratings:
        match = [
            state
            for rng, state in spaces
            if all(rmin <= v <= rmax for v, (rmin, rmax) in zip(point, rng))
        ]
        if ACCEPT in match:
            score += sum(point)
    return score


def calculate_part_1(test=False):
    lines = read(1, test=test)
    blank = lines.index("")
    rule_lines, rating_lines = lines[:blank], lines[blank + 1 :]
    rules, ratings = parse_rules(rule_lines), parse_ratings(rating_lines)
    rng = get_range(ratings)
    spaces = partition_space(rng, rules)
    return calc_score(ratings, spaces)


def calculate_part_2(test=False):
    lines = read(2, test=test)
    blank = lines.index("")
    rule_lines, rating_lines = lines[:blank], lines[blank + 1 :]
    rules = parse_rules(rule_lines)
    rng = [[1, 4000] for _ in range(4)]
    spaces = partition_space(rng, rules)
    result = 0
    for rng, state in spaces:
        if state != ACCEPT:
            continue
        result += reduce(operator.mul, (r1 - r0 + 1 for r0, r1 in rng), 1)
    return result


for part, function, test_result in [
    (1, calculate_part_1, 19114),
    (2, calculate_part_2, 167409079868000),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
