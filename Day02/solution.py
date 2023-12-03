import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def parse_max_colours(line):
    name, outcomes = line.split(":")
    id = int(name.split(" ")[1])
    max_colours = {"red": 0, "green": 0, "blue": 0}
    for game in outcomes.split(";"):
        for result in game.split(","):
            num, colour = result.strip().split(" ")
            num = int(num)
            if num > max_colours[colour]:
                max_colours[colour] = num
    return id, max_colours


def colours_within_limit(colours, max_colours):
    return all(colours[k] <= max_colours[k] for k in ("red", "green", "blue"))


def calculate_part_1(test=False):
    lines = read(1, test=test)
    parsed_lines = map(parse_max_colours, lines)
    colour_limit = {"red": 12, "green": 13, "blue": 14}
    return sum(
        id
        for id, colours in parsed_lines
        if colours_within_limit(colours, colour_limit)
    )


def calculate_part_2(test=False):
    lines = read(1, test=test)
    parsed_lines = map(parse_max_colours, lines)
    return sum(
        colours["red"] * colours["green"] * colours["blue"]
        for _, colours in parsed_lines
    )


for part, function, test_result in [
    (1, calculate_part_1, 8),
    (2, calculate_part_2, 2286),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for  part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
