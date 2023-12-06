import os


def read(part, test=False):
    this_dir = os.path.split(__file__)[0]
    name = f"input_part{part}.test" if test else "input"
    with open(os.path.join(this_dir, name), "rt") as f:
        lines = [l.strip() for l in f]
    return lines


def into_chunks(it):
    chunk = []
    for line in it:
        if line == "":
            if len(chunk) > 0:
                yield chunk
            chunk = []
        else:
            chunk.append(line)
    if len(chunk) > 0:
        yield chunk


def get_mapping(chunk):
    """Returns a list of dest, start, len tuples"""
    return [tuple(map(int, line.split())) for line in chunk if not ":" in line]


def apply_mappings_to_seed(seed, mapping):
    use_mapping = [m for m in mapping if m[1] <= seed < m[1] + m[2]]
    if len(use_mapping) == 0:
        return seed
    map_to, map_from, _ = use_mapping[0]
    return seed - map_from + map_to


def apply_mappings_to_range(seed_from, range_len, mapping):
    """Is given a range of seeds, and returns one or more ranges of seeds"""
    seed_parts = [(seed_from, seed_from + range_len - 1)]

    def split_before(pos):
        find_part = list((i, p) for i, p in enumerate(seed_parts) if p[0] < pos <= p[1])
        assert len(find_part) in (0, 1)
        if len(find_part) == 1:
            i, (s, e) = find_part[0]
            seed_parts[i : i + 1] = [(s, pos - 1), (pos, e)]

    # First split the parts based on the mapping
    for _, map_from, map_len in mapping:
        split_before(map_from)
        split_before(map_from + map_len)

    # Next, go through the parts and map them. Since they've already been "snapped"
    # in the right places, each part will move as a chunk without splitting
    def get_adjusted_part(ss, se):
        ofs = [
            map_to - map_from
            for map_to, map_from, map_len in mapping
            if map_from <= ss < map_from + map_len
        ]
        assert len(ofs) in (0, 1)
        return (ss, se) if len(ofs) == 0 else (ss + ofs[0], se + ofs[0])

    new_seed_parts = [get_adjusted_part(ss, se) for ss, se in seed_parts]
    return [(ss, se - ss + 1) for ss, se in new_seed_parts]


def apply_mappings_to_ranges(ranges, mapping):
    new_ranges = []
    for range in ranges:
        new_ranges.extend(apply_mappings_to_range(range[0], range[1], mapping))
    return new_ranges


def calculate_part_1(test=False):
    lines = read(1, test=test)
    it = iter(lines)
    seeds = [int(n) for n in next(it).split(":")[1].split()]
    for chunk in into_chunks(it):
        mapping = get_mapping(chunk)
        new_seeds = [apply_mappings_to_seed(seed, mapping) for seed in seeds]
        seeds = new_seeds
    return min(seeds)


def calculate_part_2(test=False):
    lines = read(1, test=test)
    it = iter(lines)
    seeds = [int(n) for n in next(it).split(":")[1].split()]
    ranges = list(zip(seeds[0 : len(seeds) : 2], seeds[1 : len(seeds) : 2]))
    for chunk in into_chunks(it):
        mapping = get_mapping(chunk)
        new_ranges = apply_mappings_to_ranges(ranges, mapping)
        ranges = new_ranges
    return min(s for s, l in ranges)


for part, function, test_result in [
    (1, calculate_part_1, 35),
    (2, calculate_part_2, 46),
]:
    test_answer = function(test=True)
    print(f"Part {part} (test) => {test_answer} (expecting {test_result})")
    assert test_answer == test_result, f"Test data failing for  part {part}"
    answer = function()
    print(f"Part {part} => {answer}")
