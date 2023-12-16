import os
import functools
import operator


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


def parse_map_to_effects(lines, travel_direction):
    def get_outbound(symbol):
        return functools.reduce(
            operator.or_, symbols[symbol].get(travel_direction, []), 0
        )

    vals = [list(map(get_outbound, row)) for row in lines]
    return vals


def get_path(grid, srow, scol, sdir):
    v = grid[srow] if sdir in (E, W) else [r[scol] for r in grid]
    idx = srow if sdir in (N, S) else scol
    return v[idx:] if sdir in (E, S) else v[idx::-1]


m = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
assert get_path(m, 1, 1, N) == [5, 2]
assert get_path(m, 1, 1, E) == [5, 6]
assert get_path(m, 1, 1, S) == [5, 8]
assert get_path(m, 1, 1, W) == [5, 4]


def show(state, queue):
    def num_bits(num):
        return sum(1 for d in directions if num & d > 0)

    print("\n".join("".join(str(num_bits(col)) for col in row) for row in state))
    print(f"{len(queue)}: {' '.join(f'{r},{c}->{dir_names[d]}' for r, c, d in queue)}")
    print()


def calculate_part_1(test=False):
    lines = read(1, test=test)
    maps = {d: parse_map_to_effects(lines, d) for d in (N, E, S, W)}
    return num_energised(maps, 0, 0, E)


def num_energised(maps, r0, c0, d0):
    state = [[0] * len(r) for r in maps[N]]

    def can_move(r, c, d):
        dr, dc = deltas[d]
        r, c = r + dr, c + dc
        return 0 <= r < len(state) and 0 <= c < len(state[0])

    def move(r, c, d):
        dr, dc = deltas[d]
        return r + dr, c + dc

    to_trace = [(r0, c0, d0)]
    n = 0
    while len(to_trace) > 0:
        n += 1
        trow, tcol, tdir = to_trace.pop()
        tmap = maps[tdir]
        for step in get_path(tmap, trow, tcol, tdir):
            state[trow][tcol] |= tdir
            if step > 0:
                next_dirs = (d for d in directions if can_move(trow, tcol, d))
                for nextdir in next_dirs:
                    nextrow, nextcol = move(trow, tcol, nextdir)
                    if (step & ~state[nextrow][nextcol] & nextdir) == 0:
                        continue
                    to_trace.append((nextrow, nextcol, nextdir))
                break
            trow, tcol = move(trow, tcol, tdir)
    print(f"{r0},{c0} -> {dir_names[d0]} took {n} loops")
    return sum(1 for r in state for c in r if c > 0)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    maps = {d: parse_map_to_effects(lines, d) for d in (N, E, S, W)}
    h, w = len(maps[N]), len(maps[N][0])
    starts = (
        [(0, c, S) for c in range(w)]
        + [(r, 0, E) for r in range(h)]
        + [(h - 1, c, N) for c in range(w)]
        + [(r, w - 1, W) for r in range(h)]
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
