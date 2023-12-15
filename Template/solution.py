import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def calculate_part_1(test=False):
    lines = read(1, test=test)
    return len(lines)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    return len(lines)


for part, function, test_result in [
    (1, calculate_part_1, 0),
    (2, calculate_part_2, 0),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
