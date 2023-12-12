import os
import re


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def calculate_part_1(test=False):
    lines = read(1, test=test)
    parsed = map(parse_line, lines)
    return sum(count_ways(s, l) for s, l in parsed)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    parsed = map(parse_line, lines)
    scaled = (("?".join([s] * 5), l * 5)for s, l in parsed)
    result = 0
    for i, (s, l) in enumerate(scaled, 1):
        ways = count_ways(s, l)
        print(f"{i} => {ways}")
        result += ways
    return result



def parse_line(line):
    part1, part2 = line.split()
    return part1, [int(i) for i in part2.split(",")]

def min_symbols_in(symbols):
    return sum(1 for s in symbols if s == '#')


def max_symbols_in(symbols):
    return sum(1 for s in symbols if s in ('?', '#'))

def get_options(symbols, length, symbols_before, symbols_after):
    slen = len(symbols)
    result = []
    if length > slen:
        return result
    r_str = r"[\?#]{" + str(length) + "}"
    r = re.compile(r_str)
    for _s in range(slen - length + 1):
        _e = _s + length
        if not r.fullmatch(symbols[_s:_e]):
            continue
        # Prior can't be broken, for this to be a match
        if _s > 0 and symbols[_s-1] == "#":
            continue
        # Following can't be broken, for this to be a match
        if _e < slen and symbols[_e] == "#":
            continue
        before = "" if _s < 2 else symbols[:_s-1]
        if not min_symbols_in(before) <= symbols_before <= max_symbols_in(before):
            continue
        after = "" if _e > slen - 2 else symbols[_e+1:]
        if not min_symbols_in(after) <= symbols_after <= max_symbols_in(after):
            continue
        result.append((before, after))
    return result


def count_ways(symbols, lengths):
    longest = max(lengths)
    index = lengths.index(longest)
    num_before, num_after = sum(lengths[:index]), sum(lengths[index+1:])
    options = get_options(symbols, longest, num_before, num_after)
    # If no more to locate, this is the answer
    if num_before == 0 and num_after == 0:
        return len(options)
    result = 0
    for before_symbols, after_symbols in options:
        sub_result = 1
        if num_before > 0:
            sub_result *= count_ways(before_symbols, lengths[:index])
        if num_after > 0:
            sub_result *= count_ways(after_symbols, lengths[index+1:])
        result += sub_result
    return result



for part, function, test_result in [
    (1, calculate_part_1, 21),
    (2, calculate_part_2, 525152),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
