import os

WORDS = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
NUMBER_WORDS = {word: str(idx + 1) for idx, word in enumerate(WORDS)}


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def get_numbers(line):
    digits = [char for char in line if char in NUMBER_WORDS.values()]
    return int(f"{digits[0]}{digits[-1]}")


def get_digits(line, accum=""):
    if line == "":
        return accum
    try:
        digit = next(d for w, d in NUMBER_WORDS.items() if line.startswith(w))
        return get_digits(line[1:], accum + digit)
    except StopIteration:
        if line[0] in NUMBER_WORDS.values():
            return get_digits(line[1:], accum + line[0])
        else:
            return get_digits(line[1:], accum)


def calculate_part_1(test=False):
    lines = read(1, test=test)
    return sum(map(get_numbers, lines))


def calculate_part_2(test=False):
    lines = read(2, test=test)
    converted_lines = map(get_digits, lines)
    return sum(map(get_numbers, converted_lines))


for part, function, test_result in [
    (1, calculate_part_1, 142),
    (2, calculate_part_2, 281),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for  part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
