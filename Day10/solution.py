import os
from itertools import chain


DIRECTIONS = ("N", "E", "S", "W")

SYMBOLS = {  # maps symbols to (in, out) tuples
    "|": ("NS", "NS"),
    "-": ("EW", "EW"),
    "L": ("NE", "NE"),
    "J": ("NW", "NW"),
    "7": ("SW", "SW"),
    "F": ("SE", "SE"),
    ".": ("", ""),
    "S": ("", "NSEW"),
}

# The insight here is that I'm counting the crossings just down and to the right
# of the centre of each cell. Not perfect, but since the crossing itself is always
# out, it's good enough
CROSSINGS = "|7F"

DELTAS = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}

OPPOSITES = {"N": "S", "E": "W", "S": "N", "W": "E"}


def on_board(pos, layout):
    return all(0 <= ofs < size for ofs, size in zip(pos, layout))


def get_links(pos, dimensions, layout):
    r, c = pos
    for direction in SYMBOLS[layout[r][c]][1]:
        delta_r, delta_c = DELTAS[direction]
        new_r, new_c = new_pos = (r + delta_r, c + delta_c)
        if not on_board(new_pos, dimensions):
            continue
        direction_from = OPPOSITES[direction]
        symbol = layout[new_r][new_c]
        target_in = SYMBOLS[symbol][0]
        if not direction_from in target_in:
            continue
        yield new_pos


def find_start(layout):
    r, l = next((r, l) for r, l in enumerate(layout) if "S" in l)
    return (r, l.index("S"))


def get_start_symbol(pos, dimensions, layout):
    r, c = pos
    links_to = []
    for direction in "NSEW":
        delta_r, delta_c = DELTAS[direction]
        new_r, new_c = new_pos = (r + delta_r, c + delta_c)
        if not on_board(new_pos, dimensions):
            continue
        direction_from = OPPOSITES[direction]
        symbol = layout[new_r][new_c]
        target_in = SYMBOLS[symbol][0]
        if not direction_from in target_in:
            continue
        links_to.append(direction)
    links_to = sorted("".join(links_to))
    start_symbol = [
        s for s, (s_in, s_out) in SYMBOLS.items() if sorted(s_out) == links_to
    ]
    assert len(start_symbol) == 1
    return start_symbol[0]


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def calculate_distances(lines):
    dimensions = len(lines), len(lines[0])
    start = find_start(lines)
    best = {start: 0}
    nodes = [start]
    while len(nodes) > 0:
        node, nodes = nodes[0], nodes[1:]
        next_dist = best[node] + 1
        for next_node in get_links(node, dimensions, lines):
            if next_node in best and next_dist >= best[next_node]:
                continue
            best[next_node] = next_dist
            nodes.append(next_node)
    return best


def get_dimensions(lines):
    return len(lines), len(lines[0])


def calculate_part_1(test=False):
    lines = read(1, test=test)
    distances = calculate_distances(lines)
    return max(distances.values())


def get_crossings(lines, distances):
    nrows, ncols = get_dimensions(lines)

    def get_cell(r, c):
        if (r, c) in distances:
            return lines[r][c] in CROSSINGS
        return False

    return [[get_cell(r, c) for c in range(ncols)] for r in range(nrows)]


def cum_toggles(it):
    tot = False
    for val in it:
        if val:
            tot = not tot
        yield tot


def calc_in(crossings, distance):
    num_crossings = [list(cum_toggles(row)) for row in crossings]
    result = []
    for r, row in enumerate(num_crossings):
        result_row = []
        for c, toggle in enumerate(row):
            if (r, c) in distance:
                is_in = " "
            else:
                is_in = "X" if toggle else " "
            result_row.append(is_in)
        result.append("".join(result_row))
    return result


def calculate_part_2(test=False):
    lines = read(2, test=test)
    dimensions = get_dimensions(lines)
    r, c = start = find_start(lines)
    distances = calculate_distances(lines)

    start_symbol = get_start_symbol(start, dimensions, lines)
    line = lines[r]
    lines[r] = line[:c] + start_symbol + line[c + 1 :]

    crossings = get_crossings(lines, distances)
    answer = calc_in(crossings, distances)
    return len([a for row in answer for a in row if a == "X"])


for part, function, test_result in [
    (1, calculate_part_1, 8),
    (2, calculate_part_2, 10),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
