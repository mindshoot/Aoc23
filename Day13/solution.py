import os
import functools


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def to_chunks(lines, delim=""):
    while delim in lines:
        i = lines.index(delim)
        yield lines[:i]
        lines = lines[i + 1 :]
    yield lines


def count_mismatches(line, idx):
    before, after = line[:idx], line[idx:]
    shortest = min(len(before), len(after))
    left, right = before[-shortest:], after[:shortest][::-1]
    return sum(1 for l, r in zip(left, right) if l != r)


def matching_cols(line):
    return set(i for i in range(1, len(line)) if count_mismatches(line, i) == 0)


def get_symmetry_column(chunk):
    cols = functools.reduce(set.intersection, map(matching_cols, chunk))
    assert len(cols) in (0, 1), "Unexpected number of columns"
    return cols.pop() if len(cols) > 0 else None


def get_symmetric_rows_by_col(chunk):
    rows_by_col = {}
    for r, line in enumerate(chunk):
        for c in matching_cols(line):
            rows_by_col[c] = rows_by_col.get(c, set()) | {r}
    return rows_by_col


def get_smudged_symmetry_column(chunk):
    # We need a column that matches everywhere apart from one row
    nrows = len(chunk)
    rows_by_col = get_symmetric_rows_by_col(chunk)
    cols = set()
    for test_col, rows in rows_by_col.items():
        if len(rows) != nrows - 1:
            continue  # only interested in columns where only one row didn't match
        missing_row = (set(range(nrows)) - rows).pop()
        if count_mismatches(chunk[missing_row], test_col) == 1:
            cols |= {test_col}
    assert len(cols) in (0, 1), "Unexpected number of columns"
    return cols.pop() if len(cols) > 0 else None


def transpose(chunk):
    return ["".join([l[c] for l in chunk]) for c, _ in enumerate(chunk[0])]


def calculate_part_1(test=False):
    lines = read(1, test=test)
    chunks = to_chunks(lines)
    result = 0
    for chunk in chunks:
        col = get_symmetry_column(chunk)
        if col is not None:
            result += col
        else:
            result += 100 * get_symmetry_column(transpose(chunk))
    return result


def calculate_part_2(test=False):
    lines = read(1, test=test)
    chunks = to_chunks(lines)
    result = 0
    for chunk in chunks:
        col = get_smudged_symmetry_column(chunk)
        if col is not None:
            result += col
        else:
            result += 100 * get_smudged_symmetry_column(transpose(chunk))
    return result


for part, function, test_result in [
    (1, calculate_part_1, 405),
    (2, calculate_part_2, 400),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
