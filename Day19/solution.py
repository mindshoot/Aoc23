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


assert parse_rating("{x=787,m=2655,a=1222,s=2876}") == [787, 2655, 1222, 2876], "Rating parsing broken"
assert parse_ratings(["{x=787,m=2655,a=1222,s=2876}"]) == [[787, 2655, 1222, 2876]], "Rating parsing broken"


TEST_RULE = "px{a<2006:qkq,m>2090:A,rfg}"
TEST_RULE_PARSED = ('px', [(2, "<", 2006, "qkq"), (1, ">", 2090, ACCEPT), (None, None, None, "rfg")])

assert parse_rule(TEST_RULE) == TEST_RULE_PARSED, "rule parsing broken"
assert parse_rules([TEST_RULE]) == {TEST_RULE_PARSED[0]: TEST_RULE_PARSED[1]}, "rule assembly broken"


def get_range(ratings):
    cols = [[r[c] for r in ratings] for c in range(4)]
    return [[min(col), max(col)] for col in cols]


assert get_range([(1, 2, 3, 4), (9, 8, 7, 1)]) == [[1, 9], [2, 8], [3, 7], [1, 4]], "ratings broken"


def partition_space(range, rules):
    spaces = [(range, "?")]
    queue = [(0, "in", 0)]

    def show_stats():
        vols = {}
        for range, state in spaces:
            v = reduce(operator.mul, (r1 - r0 + 1 for r0, r1 in range), 1)
            vols[state] = vols.get(state, 0) + v
        print(f"{len(spaces)} spaces, total volume {sum(vols.values())}, queue length {len(queue)}")
        print(vols)

    while len(queue) > 0:
        # show_stats()
        # All spaces that are "?" should be in the queue

        in_queue = {i for i, _, _ in queue}
        awaiting_decision = {i for i, (_, state) in enumerate(spaces) if state == "?"}
        if in_queue != awaiting_decision:
            print(f"Have lost: {awaiting_decision - in_queue}")

        (index, key, ofs), queue = queue[0], queue[1:]

        print(f"Working on space #{index}, currently at '{key}', {ofs}")

        rng, state = spaces[index]
        if key in {ACCEPT, REJECT}:
            print(f"space #{index} -> {key}")
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
        elif (condition == ">" and rmax <= value) or (condition == "<" and rmin >= value):
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
            if i is None:
                print("HELP!")
            queue.append((i, outcome, 0))
        # Process the range that doesn't meet the condition
        if this_result == False or (this_result == True and new_idx is not None):
            i = new_idx if this_result else index
            if i is None:
                print("HELP!")
            new_key, new_ofs = (key, ofs + 1) if ofs + 1 < len(rules[key]) else (outcome, 0)
            queue.append((i, new_key, new_ofs))

    return spaces


def calc_score(ratings, spaces):
    score = 0
    for point in ratings:
        match = [state for rng, state in spaces if all(rmin <= v <= rmax for v, (rmin, rmax) in zip(point, rng))]
        assert len(match) == 1
        if ACCEPT in match:
            score += sum(point)
    return score



def calculate_part_1(test=False):
    lines = read(1, test=test)
    blank = lines.index("")
    rule_lines, rating_lines = lines[:blank], lines[blank+1:]
    rules, ratings = parse_rules(rule_lines), parse_ratings(rating_lines)
    rng = get_range(ratings)
    spaces = partition_space(rng, rules)
    return calc_score(ratings, spaces)


def calculate_part_2(test=False):
    lines = read(2, test=test)
    blank = lines.index("")
    rule_lines, rating_lines = lines[:blank], lines[blank+1:]
    rules, ratings = parse_rules(rule_lines), parse_ratings(rating_lines)
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
