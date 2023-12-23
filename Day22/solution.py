import os
import itertools


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def parse_coord(val):
    return tuple(map(int, val.split(",")))  # -> x,y,z


def parse_line(line):
    coords = tuple(map(parse_coord, line.split("~")))
    xs, ys, zs = zip(coords[0], coords[1])
    assert xs[0] == xs[1] or ys[0] == ys[1] or zs[0] == zs[1]
    return coords


def get_base(blocks):
    coords = (v[1:] for v in blocks)
    fields = itertools.chain(*coords)
    xs, ys, _ = zip(*fields)
    xl, xh = min(xs), max(xs)
    yl, yh = min(ys), max(ys)
    assert 0 <= xl <= xh, "Invalid x range"
    assert 0 <= yl <= yh, "Invalid y range"
    return xh, yh


def iterate_grid(xs, ys):
    (x0, x1), (y0, y1) = xs, ys
    if x0 == x1:
        yl, yh = (y0, y1) if y0 <= y1 else (y1, y0)
        return ((x0, y) for y in range(yl, yh + 1))
    if y0 == y1:
        xl, xh = (x0, x1) if x0 <= x1 else (x1, x0)
        return ((x, y0) for x in range(xl, xh + 1))
    assert False, "This should never happen"


def validate_blocks(blocks):
    for _, p1, p2 in blocks:
        (x1, x2), (y1, y2), (z1, z2) = zip(p1, p2)
        assert 0 <= x1 <= x2
        assert 0 <= y1 <= y2
        assert 0 <= z1 <= z2
        assert x1 == x2 or y1 == y2 or z1 == z2


def get_supports(blocks):
    xmax, ymax = get_base(blocks)
    heights = [[0 for _ in range(xmax + 1)] for _ in range(ymax + 1)]
    tops = [[None for _ in range(xmax + 1)] for _ in range(ymax + 1)]
    supported_by = {}
    for id, end1, end2 in blocks:
        xs, ys, zs = zip(end1, end2)
        this_height = zs[1] - zs[0] + 1
        max_height = max(heights[y][x] for x, y in iterate_grid(xs, ys))
        if max_height > 0:
            resting_on = set(
                tops[y][x]
                for x, y in iterate_grid(xs, ys)
                if heights[y][x] == max_height
            )
        else:
            resting_on = set()
        for x, y in iterate_grid(xs, ys):
            heights[y][x] = max_height + this_height
            tops[y][x] = id
        supported_by[id] = resting_on
    return supported_by


def calculate_part_1(test=False):
    lines = read(1, test=test)
    blocks = sorted(
        ((i, *parse_line(l)) for i, l in enumerate(lines)), key=lambda b: b[1][2]
    )
    supported_by = get_supports(blocks)

    sole_supports = {next(iter(r)) for r in supported_by.values() if len(r) == 1}
    return len(supported_by.keys() - sole_supports)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    blocks = sorted(
        ((i, *parse_line(l)) for i, l in enumerate(lines)), key=lambda b: b[1][2]
    )
    sat_on = get_supports(blocks)
    zappable = {k for k, v in sat_on.items() if len(v) > 0}

    def disintegrate(id):
        gone = {id}
        while True:
            new_gone = {b for b in zappable - gone if all(s in gone for s in sat_on[b])}
            if len(new_gone) == 0:
                break
            gone |= new_gone
        return len(gone - {id})

    sole_supports = {next(iter(r)) for r in sat_on.values() if len(r) == 1}
    return sum(map(disintegrate, sole_supports))


if __name__ == "__main__":
    for part, function, test_result in [
        (1, calculate_part_1, 5),
        (2, calculate_part_2, 7),
    ]:
        if test_result is not None:
            test_answer = function(test=True)
            print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
            assert (
                test_answer == test_result
            ), f"{test_result} != {test_answer}, test failing for part {part}"
        answer = function()
        print(f"Part {part} => {answer}")
