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

    def get_options(self, row, col, dirn, count):
        opts = self.OPTIONS[dirn]
        yield from ((d, 1) for d in opts if d != dirn and self.can_move(row, col, d))
        if count < 3 and self.can_move(row, col, dirn):
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
    best = m.make_data(lambda r, c: {})
    to_eval = []
    heapq.heappush(to_eval, (0, 0, 0, E, 1)) # score, row, col, dirn, count
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
        check_scores = list(cell_bests.get((dr, i)) for i in range(1, num+1) if (dr, i) in cell_bests)
        if len(check_scores) == 0 or nscore < min(check_scores):
            best[nrow][ncol][(dr, num)] = nscore
            for edir, ecount in m.get_options(nrow, ncol, dr, num):
                item = (nscore, nrow, ncol, edir, ecount)
                heapq.heappush(to_eval, item)
    return min(best[m.height - 1][m.width - 1].values())


def calculate_part_2(test=False):
    lines = read(1, test=test)
    return len(lines)


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
