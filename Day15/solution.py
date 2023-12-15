import os
import functools


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
    boxes = {box_no: {} for box_no in range(256)}

    def add_or_replace(index, code, length):
        box = boxes[get_hash(code)]
        box[code] = (length, box.get(code, (None, index))[1])

    def remove(code):
        box = boxes[get_hash(code)]
        if code in box:
            del box[code]

    for i, part in enumerate(parts):
        if "-" in part:
            remove(part[:-1])
        else:
            add_or_replace(i, *part.split("="))

    def get_power(box_no):
        in_box = sorted(boxes[box_no].values(), key=lambda e: e[1])
        return sum((box_no + 1) * r * int(p) for r, (p, _) in enumerate(in_box, 1))

    return sum(map(get_power, range(256)))


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
