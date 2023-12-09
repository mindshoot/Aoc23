import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def to_numbers(line):
    return list(map(int, line.split()))


def predict_next(series):
    diffs = list(s2 - s1 for s1, s2 in zip(series, series[1:]))
    if all(d == 0 for d in diffs):
        return series[-1]
    return series[-1] + predict_next(diffs)


def predict_previous(series):
    diffs = list(s2 - s1 for s1, s2 in zip(series, series[1:]))
    if all(d == 0 for d in diffs):
        return series[0]
    return series[0] - predict_previous(diffs)


def calculate_part_1(test=False):
    lines = read(1, test=test)
    numbers = map(to_numbers, lines)
    predictions = map(predict_next, numbers)
    return sum(predictions)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    numbers = map(to_numbers, lines)
    predictions = map(predict_previous, numbers)
    return sum(predictions)


for part, function, test_result in [
    (1, calculate_part_1, 114),
    (2, calculate_part_2, 2),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
