import os
import heapq
from collections import Counter


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
        return self.lines[r][c]

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


def take_steps(lines, steps):
    m = Map(lines)

    # Find the start
    positions = {
        (r, c)
        for r, line in enumerate(lines)
        for c, symbol in enumerate(line)
        if symbol == "S"
    }
    results = [positions]
    for _ in range(steps):
        adjacent = {
            m.move(r, c, d)
            for r, c in positions
            for d in directions
            if m.can_move(r, c, d)
        }
        positions = {(r, c) for r, c in adjacent if m.get(r, c) != "#"}
        results.append(positions)

    return results


def take_more_steps(lines, steps):
    nrows, ncols = len(lines), len(lines[0])

    def is_rock(r, c):
        return lines[r % nrows][c % ncols] == "#"

    positions = {
        (r, c)
        for r, line in enumerate(lines)
        for c, symbol in enumerate(line)
        if symbol == "S"
    }

    def print_positions(step_num):
        tile_rows, tile_cols = 3, 7
        rofs, cofs = nrows * (tile_rows // 2), 0  # ncols * (tile_cols // 2)
        points = [
            [
                "x"
                if (r - rofs, c - cofs) in positions
                else lines[(r - rofs) % nrows][(c - cofs) % ncols]
                for c in range(ncols * tile_cols)
            ]
            for r in range(nrows * tile_rows)
        ]
        print(f"=== Step {step_num} ===")
        print("\n".join("".join(row) for row in points))

    def num_in_rows(step_num):
        counts = (
            len({c for c, r in positions if r == row})
            for row in range(-nrows, 2 * nrows + 1)
        )
        info = " ".join(f"{n:<3}" for n in counts)
        print(f"Step {step_num:<3}: {info}")

    size = 5

    def num_in_tiles(step_num):
        print(f"Step 65 + {(step_num - 65) // 131} * 131 [{step_num}]")
        c = Counter()
        for trow in range(-size, size + 1):
            rmin, rmax = trow * nrows, (trow + 1) * nrows - 1
            line = []
            for tcol in range(-size, size + 1):
                cmin, cmax = tcol * ncols, (tcol + 1) * ncols - 1
                num = sum(
                    1 for r, c in positions if rmin <= r <= rmax and cmin <= c <= cmax
                )
                c.update([num])
                line.append(f"{num:<4}")
            print(" ".join(line))
        print(sorted(c.most_common()))
        print(sum(k * v for k, v in c.items()))

    def num_in_tile(step_num, trow=0, tcol=0):
        rmin, rmax = trow * nrows, (trow + 1) * nrows - 1
        cmin, cmax = tcol * ncols, (tcol + 1) * ncols - 1
        num = sum(1 for r, c in positions if rmin <= r <= rmax and cmin <= c <= cmax)
        print(f"({trow},{tcol}) [{step_num}]={num}")

    def debug(step_num):
        if (step_num - 65) % 131 == 0:
            # if step_num % 1 == 0:
            num_in_tiles(step_num)
            # num_in_tile(step_num // 1, -1, 0)

    debug(0)

    deltas = list(Coords.DELTAS.values())
    for step_num in range(1, steps + 1):
        positions = set(
            (r + dr, c + dc)
            for r, c in positions
            for dr, dc in deltas
            if not is_rock(r + dr, c + dc)
        )
        debug(step_num)
    return positions


def calculate_part_1(test=False):
    lines = read(1, test=test)
    num_steps = 6 if test else 64
    results = take_steps(lines, num_steps)
    return len(results[num_steps])


def calculate_part_2(test=False):
    lines = read(1, test=test)
    num_steps = 100 if test else 26501365
    results = take_more_steps(lines, num_steps)
    return len(results)


for part, function, test_result in [
    (1, calculate_part_1, 16),
    (2, calculate_part_2, None),
]:
    if test_result is not None:
        test_answer = function(test=True)
        print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
        assert (
            test_answer == test_result
        ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
