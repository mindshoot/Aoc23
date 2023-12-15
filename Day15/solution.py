import os
import functools
from collections import OrderedDict


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def as_parts(lines):
    return lines[0].split(",")


def add_to_hash(orig, char):
    return ((orig + ord(char)) * 17) % 256


def get_hash(string):
    return functools.reduce(add_to_hash, string, 0)


def calculate_part_1(test=False):
    parts = as_parts(read(1, test=test))
    return sum(map(get_hash, parts))


def calculate_part_2(test=False):
    parts = as_parts(read(1, test=test))
    boxes = {box_no: OrderedDict() for box_no in range(256)}

    def add_or_replace(instruction):
        code, length = instruction.split("=")
        boxes[get_hash(code)][code] = length

    def remove(instruction):
        code = instruction[:-1]
        boxes[get_hash(code)].pop(code, None)

    for part in parts:
        (add_or_replace if "=" in part else remove)(part)

    def get_power(box_no):
        contents = boxes[box_no].values()
        return sum((box_no + 1) * r * int(p) for r, p in enumerate(contents, 1))

    return sum(map(get_power, boxes.keys()))


for part, function, test_result in [
    (1, calculate_part_1, 1320),
    (2, calculate_part_2, 145),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
