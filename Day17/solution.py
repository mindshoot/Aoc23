import os
import heapq

directions = N, E, S, W = "N", "E", "S", "W"

deltas = {N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)}

dir_names = {N: "north", E: "east", S: "south", W: "west"}


class Map:
    DELTAS = {N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)}

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
        drow, dcol = self.DELTAS[dirn]
        return 0 <= row + drow < self.height and 0 <= col + dcol < self.width

    def move(self, row, col, dirn):
        dr, dc = self.DELTAS[dirn]
        return row + dr, col + dc

    def make_data(self, fn):
        return [[fn(r, c) for c in range(self.width)] for r in range(self.height)]


class Day17Map(Map):
    OPTIONS = {N: [N, W, E], E: [E, N, S], S: [S, W, E], W: [W, N, S]}

    def get_options(self, row, col, dirn, count, min_straight=1, max_straight=3):
        opts = self.OPTIONS[dirn]
        if count >= min_straight:
            yield from (
                (d, 1) for d in opts if d != dirn and self.can_move(row, col, d)
            )
        if count < max_straight and self.can_move(row, col, dirn):
            yield (dirn, count + 1)


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def calculate_part_1(test=False):
    lines = read(1, test=test)
    m = Day17Map(lines)
    best = run_calc(m, smin=1, smax=3)
    return min(best[m.height - 1][m.width - 1].values())


def run_calc(m, smin, smax):
    best = m.make_data(lambda r, c: {})
    to_eval = []
    heapq.heappush(to_eval, (0, 0, 0, E, 1))  # score, row, col, dirn, count
    heapq.heappush(to_eval, (0, 0, 0, S, 1))
    n, l = 0, 0
    while len(to_eval) > 0:
        n += 1
        if n >= l + 10000:
            print(f"Iteration {n}, {len(to_eval)} in queue")
            l += 10000
        score, row, col, dr, num = heapq.heappop(to_eval)
        nrow, ncol = m.move(row, col, dr)
        nscore = score + m.get(nrow, ncol)
        cell_bests = best[nrow][ncol]
        check_scores = list(
            cell_bests.get((dr, i)) for i in [num] if (dr, i) in cell_bests
        )  # range(1, num + 1)
        if len(check_scores) == 0 or nscore < min(check_scores):
            best[nrow][ncol][(dr, num)] = nscore
            for edir, ecount in m.get_options(
                nrow, ncol, dr, num, min_straight=smin, max_straight=smax
            ):
                item = (nscore, nrow, ncol, edir, ecount)
                heapq.heappush(to_eval, item)
    return best


def calculate_part_2(test=False):
    lines = read(1, test=test)
    m = Day17Map(lines)
    best = run_calc(m, smin=4, smax=10)
    # Given the barb in the tail that even the final run needs to be 4-10 straight, the best will be
    # based on things hitting the bottom edge between 4 and 10 from the corner, or the right side
    # Extra score to go straight across by cell
    row_data = [m.get(m.last_row, c) for c in range(m.width)]
    row_best = [
        min(v for k, v in c.items() if k[0] == "S" and k[1] >= 4)
        for c in m.get_row(m.last_row, best)
    ]
    adj = [sum(row_data[c:]) - v for c, v in enumerate(row_data)]
    row_best_adj = [b + a for b, a in zip(row_best, adj)]
    res1 = min(row_best_adj[-11:-4])

    col_data = [m.get(r, m.last_col) for r in range(m.height)]
    col_best = [
        min(v for k, v in c.items() if k[0] == "E" and k[1] >= 4)
        for c in m.get_col(m.last_col, best)
    ]
    adj = [sum(col_data[r:]) - v for r, v in enumerate(col_data)]
    col_best_adj = [b + a for b, a in zip(col_best, adj)]
    res2 = min(col_best_adj[-11:-4])
    return min(res1, res2)


for part, function, test_result in [
    (1, calculate_part_1, 102),
    (2, calculate_part_2, 94),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
