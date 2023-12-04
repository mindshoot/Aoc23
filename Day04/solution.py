import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def split(val):
    return [int(v) for v in val.strip().split()]


def parse_card(line):
    card, numbers = line.split(":")
    winning, actual = numbers.split("|")
    return card, split(winning), split(actual)


def count_winners(winning, actual):
    return len([a for a in actual if a in winning])


def score_winning(winning, actual):
    num_winners = count_winners(winning, actual)
    return pow(2, num_winners - 1) if num_winners > 0 else 0


def calculate_part_1(test=False):
    lines = read(1, test=test)
    parsed = map(parse_card, lines)
    scores = map(lambda p: score_winning(p[1], p[2]), parsed)
    return sum(scores)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    parsed = map(parse_card, lines)
    num_winners = [count_winners(winning, actual) for _, winning, actual in parsed]
    multipliers = [1] * len(num_winners)
    for idx, (num_win, mult) in enumerate(zip(num_winners, multipliers)):
        if num_win == 0:
            continue
        for ofs, _ in enumerate(multipliers[idx + 1 : idx + num_win + 1]):
            multipliers[idx + ofs + 1] += mult
    return sum(multipliers)


for part, function, test_result in [
    (1, calculate_part_1, 13),
    (2, calculate_part_2, 30),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for  part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
