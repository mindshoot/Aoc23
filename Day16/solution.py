import os
from functools import reduce
from itertools import chain
from operator import or_


directions = N, E, S, W = 1, 2, 4, 8

symbols = {
    ".": {},
    "/": {N: [E], E: [N], S: [W], W: [S]},
    "\\": {N: [W], E: [S], S: [E], W: [N]},
    "|": {E: [N, S], W: [N, S]},
    "-": {N: [E, W], S: [E, W]},
}

deltas = {N: (-1, 0), E: (0, 1), S: (1, 0), W: (0, -1)}

dir_names = {N: "north", E: "east", S: "south", W: "west"}


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def parse_map_to_outbound(lines, d):
    def get_outbound(symbol):
        return reduce(or_, symbols[symbol].get(d, []), 0)

    vals = [list(map(get_outbound, row)) for row in lines]
    return vals


def get_path(grid, srow, scol, sdir):
    v = grid[srow] if sdir in (E, W) else [r[scol] for r in grid]
    idx = srow if sdir in (N, S) else scol
    return v[idx:] if sdir in (E, S) else v[idx::-1]


def num_energised(maps, r0, c0, d0):
    state = [[0] * len(r) for r in maps[N]]
    h, w = len(state), len(state[0])

    def can_move(r, c, d):
        dr, dc = deltas[d]
        return 0 <= r + dr < h and 0 <= c + dc < w

    def move(r, c, d):
        dr, dc = deltas[d]
        return r + dr, c + dc

    n = 0
    trace_queue = [(r0, c0, d0)]
    while len(trace_queue) > 0:
        n += 1
        trow, tcol, tdir = trace_queue.pop()
        tmap = maps[tdir]
        for new_directions in get_path(tmap, trow, tcol, tdir):
            state[trow][tcol] |= tdir
            if new_directions > 0:
                for ndir in (d for d in directions if can_move(trow, tcol, d)):
                    nrow, ncol = move(trow, tcol, ndir)
                    if (new_directions & ~state[nrow][ncol] & ndir) != 0:
                        trace_queue.append((nrow, ncol, ndir))
                break
            trow, tcol = move(trow, tcol, tdir)
    print(f"{r0},{c0} -> {dir_names[d0]} took {n} loops")
    return sum(1 for r in state for c in r if c > 0)


def calculate_part_1(test=False):
    lines = read(1, test=test)
    maps = {d: parse_map_to_outbound(lines, d) for d in (N, E, S, W)}
    return num_energised(maps, 0, 0, E)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    maps = {d: parse_map_to_outbound(lines, d) for d in (N, E, S, W)}
    h, w = len(maps[N]), len(maps[N][0])
    starts = chain(
        *[[(0, c, S), (h - 1, c, N)] for c in list(range(0, h))],
        *[[(r, 0, E), (r, w - 1, W)] for r in list(range(0, w))],
    )
    calculate = lambda x: num_energised(maps, *x)
    return max(map(calculate, starts))


for part, function, test_result in [
    (1, calculate_part_1, 46),
    (2, calculate_part_2, 51),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert (
        test_answer == test_result
    ), f"{test_result} != {test_answer}, test failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
