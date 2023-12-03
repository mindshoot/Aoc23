import os
import re
from itertools import tee, chain

NUMBER_RE = re.compile(r"[1-9][0-9]*")


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def get_numbers_and_positions(line):
    for match in NUMBER_RE.finditer(line):
        s, n = match.span()
        number = int(match.group(0))
        yield number, s, n


def has_symbol_near(line, first_char, following_char):
    """Are there symbols on this line adjacent to the word?"""
    adj = line[max(first_char - 1, 0) : following_char + 1]
    symbols = [a for a in adj if a not in "1234567890."]
    return len(symbols) > 0


def iter_in_threes(it):
    i1, i2, i3 = tee(it, 3)
    next(i3)
    return zip(
        chain([None], i1),
        i2,
        chain(i3, [None]),
    )


def get_parts_in_line(prev_line, line, next_line):
    """Pull out part numbers - numbers with symbols nearby"""
    for part_no, first, following in get_numbers_and_positions(line):
        if has_symbol_near(line, first, following):
            yield part_no
        elif prev_line is not None and has_symbol_near(prev_line, first, following):
            yield part_no
        elif next_line is not None and has_symbol_near(next_line, first, following):
            yield part_no


def get_star_positions(line, first, following):
    """Where are the stars adjacent to the specified position?"""
    start = max(first - 1, 0)
    bit_to_check = line[start : following + 1]
    return [start + i for i, c in enumerate(bit_to_check) if c == "*"]


def get_stars_around_numbers(line_no, prev_line, line, next_line):
    for part_no, first, following in get_numbers_and_positions(line):
        number_info = line_no, first, part_no
        for check_line, line_offset in [(prev_line, -1), (line, 0), (next_line, 1)]:
            if check_line is None:
                continue
            for star_position in get_star_positions(check_line, first, following):
                star_info = line_no + line_offset, star_position
                yield number_info, star_info


def calculate_part_1(test=False):
    lines = read(1, test=test)
    total = 0
    for prev_line, line, next_line in iter_in_threes(lines):
        total += sum(get_parts_in_line(prev_line, line, next_line))
    return total


def calculate_part_2(test=False):
    lines = read(2, test=test)
    stars = {}
    for idx, (prev_line, line, next_line) in enumerate(iter_in_threes(lines)):
        for number_info, star_info in get_stars_around_numbers(
            idx, prev_line, line, next_line
        ):
            if star_info in stars:
                stars[star_info].append(number_info)
            else:
                stars[star_info] = [number_info]
    total = sum(
        numbers[0][2] * numbers[1][2]
        for star, numbers in stars.items()
        if len(numbers) == 2
    )
    return total


for part, function, test_result in [
    (1, calculate_part_1, 4361),
    (2, calculate_part_2, 467835),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for  part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
