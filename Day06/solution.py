import os
from math import sqrt


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def get_games(lines):
    def get_numbers(line):
        return map(int, line.split()[1:])

    return zip(get_numbers(lines[0]), get_numbers(lines[1]))


def get_games_2(lines):
    def get_numbers(line):
        val = line.split(":")[1].replace(" ", "")
        return [int(val)]

    return zip(get_numbers(lines[0]), get_numbers(lines[1]))


def solve(t, r):
    """
    To get the record distance:
    press * (time - press) = distance
    At both extremes, distance = 0, so if a win is possible then find where distance = record
    p (t - p) = r => pt - p^2 = r => p^2 - pt + r = 0
    p = (t +- sqrt(t^2 - 4r)) / 2
    """
    root = sqrt(t * t - 4 * r)
    return (t - root) / 2, (t + root) / 2


def ints_between(f1, f2):
    min_int = int(f1) + 1
    max_int = int(f2) - (1 if f2 == int(f2) else 0)
    return max_int - min_int + 1


def calculate_part_1(test=False):
    lines = read(1, test=test)
    result = 1
    games = get_games(lines)
    for time, record in games:
        min_time, max_time = solve(time, record)
        num_solutions = ints_between(min_time, max_time)
        result *= num_solutions
    return result


def calculate_part_2(test=False):
    lines = read(1, test=test)
    result = 1
    games = get_games_2(lines)
    for time, record in games:
        min_time, max_time = solve(time, record)
        num_solutions = ints_between(min_time, max_time)
        result *= num_solutions
    return result


for part, function, test_result in [
    (1, calculate_part_1, 288),
    (2, calculate_part_2, 71503),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
