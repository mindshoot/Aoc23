import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def locate_stars(l):
    stars = ((r, c) for r, rv in enumerate(l) for c, cv in enumerate(rv) if cv == "#")
    return {n: pos for n, pos in enumerate(stars, 1)}


def missing(vals):
    return set(range(min(vals), max(vals) + 1)) - vals


def find_missing(stars):
    rows = set(r for r, _ in stars.values())
    cols = set(c for _, c in stars.values())
    return missing(rows), missing(cols)


def count_steps(point1, point2, extra_rows, extra_cols, scaling=2):
    (r1, c1), (r2, c2) = point1, point2
    rmin, rmax, cmin, cmax = min(r1, r2), max(r1, r2), min(c1, c2), max(c1, c2)
    distance = abs(r2 - r1) + abs(c2 - c1)
    distance += (scaling - 1) * len([r for r in extra_rows if rmin < r < rmax])
    distance += (scaling - 1) * len([c for c in extra_cols if cmin < c < cmax])
    return distance


def calculate_part_1(test=False):
    lines = read(1, test=test)
    stars = locate_stars(lines)
    r_warped, c_warped = find_missing(stars)

    def dist(s1, s2):
        return count_steps(stars[s1], stars[s2], r_warped, c_warped)

    return sum(dist(s1, s2) for s1 in stars for s2 in stars if s2 > s1)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    stars = locate_stars(lines)
    r_warped, c_warped = find_missing(stars)

    def dist(s1, s2):
        return count_steps(stars[s1], stars[s2], r_warped, c_warped, scaling=1_000_000)

    return sum(dist(s1, s2) for s1 in stars for s2 in stars if s2 > s1)


for part, function, test_result in [
    (1, calculate_part_1, 374),
    (2, calculate_part_2, 82000210),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
