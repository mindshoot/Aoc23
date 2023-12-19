import os


directions = N, E, S, W = 1, 2, 4, 8

direction_map = {"L": W, "R": E, "U": N, "D": S}


class Coords:
    DELTAS = {N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)}
    OPPOSITES = {N: S, E: W, S: N, W: E}

    @staticmethod
    def move(row, col, dirn, count=1):
        dr, dc = Coords.DELTAS[dirn]
        return row + count * dr, col + count * dc

    @staticmethod
    def opposite(dirn):
        return Coords.OPPOSITES[dirn]


class Map(Coords):
    def __init__(self, lines):
        self.lines = lines
        self.width, self.height = len(lines[0]), len(lines)
        self.last_col, self.last_row = self.width - 1, self.height - 1

    def get_row(self, r, data=None):
        return (data or self.lines)[r]

    def get_col(self, c, data=None):
        return [l[c] for l in (data or self.lines)]

    def get(self, r, c):
        return int(self.lines[r][c])

    def can_move(self, row, col, dirn):
        r2, c2 = self.move(row, col, dirn)
        return 0 <= r2 < self.height and 0 <= c2 < self.width

    def make_data(self, fn):
        return [[fn(r, c) for c in range(self.width)] for r in range(self.height)]


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def parse(line):
    direction, count, colour = line.split()
    return direction_map[direction], int(count), colour[1:-1]


def get_transits(instrucs):
    r = c = 0
    steps = (d for d, s, _ in instrucs for _ in range(s))
    for d in steps:
        yield r, c, d
        r, c = Coords.move(r, c, d)
        yield r, c, Coords.opposite(d)


def get_range(vals):
    v = set(vals)
    vlow, vhigh = min(v), max(v)
    return vlow, vhigh, vhigh - vlow + 1


def plot_exits(instrucs):
    transits = list(get_transits(instrucs))
    rmin, _, rrange = get_range(r for r, _, _ in transits)
    cmin, _, crange = get_range(c for _, c, _ in transits)
    grid = [[0 for _ in range(crange)] for r in range(rrange)]
    for r, c, d in transits:
        grid[r - rmin][c - cmin] |= d
    """
    print("Grid")
    print("\n".join("".join("x" if c > 0 else " " for c in r) for r in grid))
    """
    return grid


def fill_grid(grid):
    output = []
    for row in grid:
        out_row = []
        inside = False
        for transit in row:
            inside = inside ^ (S & transit)
            out_row.append(1 if inside | transit > 0 else 0)
        output.append(out_row)
    """
    print("Filled")
    print(
        "\n".join(
            "".join(
                "?" if b > 0 and f == 0 else "x" if b > 0 else "." if f > 0 else " "
                for b, f in zip(br, fr)
            )
            for br, fr in zip(grid, output)
        )
    )
    """
    return output


def calculate_part_1(test=False):
    lines = read(1, test=test)
    instrucs = list(map(parse, lines))
    grid = plot_exits(instrucs)
    filled = fill_grid(grid)
    return sum(c for r in filled for c in r)


def parse2(line):
    parts = line.split()
    dist, dirn = parts[2][2:-2], parts[2][-2:-1]
    return {"0": E, "1": S, "2": W, "3": N}[dirn], int(dist, 16)


def to_polygon(instrucs):
    r = c = 0
    for dirn, count in instrucs:
        r2, c2 = Coords.move(r, c, dirn, count)
        yield (r, c, r2, c2) if r2 >= r and c2 >= c else (r2, c2, r, c)
        r, c = r2, c2


def get_polygon_area(vertices):
    """
    NB all lines are horizontal / vertical, so don't need to worry about angles 'n stuff
    """
    distinct_rows, distinct_cols = set(), set()
    for r1, c1, r2, c2 in vertices:
        distinct_rows |= {r1, r2}
        distinct_cols |= {c1, c2}
    sorted_rows = sorted(distinct_rows)
    sorted_cols = sorted(distinct_cols)
    all_dims = []
    for firstrow, lastrow in zip(sorted_rows[:-1], sorted_rows[1:]):
        row_dims = []
        for firstcol, lastcol in zip(sorted_cols[:-1], sorted_cols[1:]):
            cols_left = sum(1 for r1, c1, r2, c2 in vertices if c1 == c2 and c1 <= firstcol and r1 < lastrow and r2 > firstrow)
            if cols_left % 2 == 0:
                row_dims.append(None)
                continue
            rows_above = sum(1 for r1, c1, r2, c2 in vertices if r1 == r2 and r1 <= firstrow and c1 < lastcol and c2 > firstcol)
            if rows_above % 2 == 0:
                row_dims.append(None)
                continue
            row_dims.append((lastrow - firstrow, lastcol - firstcol))
        all_dims.append(row_dims + [None])
    all_dims.append([None] * len(all_dims[0]))

    area = sum(c[0] * c[1] for r in all_dims for c in r if c is not None)

    for r in range(len(all_dims)):
        for c in range(len(all_dims[0])):
            # Work out whether left (l), corner (c) and/or top (t) encroach
            le, co, to = False, False, False
            if all_dims[r][c] is None:
                if c > 0:
                    le = all_dims[r][c-1] is not None
                if r > 0:
                    to = all_dims[r-1][c] is not None
                if r > 0 and c > 0:
                    co = all_dims[r][c-1] is None and all_dims[r-1][c] is None and all_dims[r-1][c-1] is not None
            if le:
                delta = all_dims[r][c-1][0] - 1
                print(f"Adding {delta} on left")
                area += delta
            if to:
                delta = all_dims[r-1][c][1] - 1
                print(f"Adding {delta} on top")
                area += delta
            if le or to or co:
                delta = 1
                print(f"Adding {delta} on corner")
                area += delta

    return area

"""


    # Add a strip to the right hand side for all boxes without another on their right
    for row in all_dims:
        for col, next_col in zip(row, row[1:]):
            if next_col is None and col is not None:
                area += col[0]

    # Add a strip to the bottom side for all boxes without another below them
    for c, _ in enumerate(all_dims[0]):
        col = [r[c] for r in all_dims]
        for row, next_row in zip(col, col[1:]):
            if next_row is None and row is not None:
                area += row[1]

    # Add one to the bottom side for all boxes without another below them, ie
    # count the cells that are null, and left / right is null, but above-left isn't

    for r, _ in enumerate(all_dims):
        for c, _ in enumerate(all_dims[0]):
            if all_dims[r][c] is not None:
                continue
            if r == 0:
                continue
            if c == 0:
                continue
            if all_dims[r-1][c] is not None:
                continue
            if all_dims[r][c-1] is not None:
                continue
            if all_dims[r-1][c-1] is None:
                continue
            area += 1

"""



def calculate_part_2(test=False):
    lines = read(1, test=test)
    instrucs = map(parse2, lines)
    vertices = list(to_polygon(instrucs))
    return get_polygon_area(vertices)


for part, function, test_result in [
    #(1, calculate_part_1, 62),
    (2, calculate_part_2, 952408144115),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
