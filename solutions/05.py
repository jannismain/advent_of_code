#!/usr/bin/env python

from itertools import chain


# disable print log statements for performance reasons
class Devnull(object):
    def write(self, *_):
        pass


log = Devnull()


def parse(data: str):
    rv = {}
    s, ss, sf, fw, wl, lt, th, hl = data.split("\n\n")
    rv["s"] = [int(x) for x in s.split(": ")[1].split()]
    for m in "ss sf fw wl lt th hl".split():
        n = locals()[m]
        rv[m] = [tuple(int(x) for x in line.split()) for line in n.splitlines()[1:]]
        # convert (dest, src, width) to (src_start, src_end, offset)
        rv[m] = [(t[1], t[1] + t[2], t[0] - t[1]) for t in rv[m]]

    # print parsed data in readable format
    for k, mp in rv.items():
        print(k, file=log)
        for m in mp:
            print(" ", m, file=log)
    return rv


def main(data):
    if isinstance(data, str):
        data = parse(data)
    min_location = float("inf")
    for seed in data.pop("s"):
        print(f"\nSeed {seed}", end="", file=log)
        loc = seed
        for mapping_name, mapping_list in data.items():
            print(f" -{mapping_name}", end="", file=log)
            for mapping in mapping_list:
                src_start, src_end, offset = mapping
                if src_start <= loc < src_end:
                    loc += offset
                    print(f"-> {loc}", end="", file=log)
                    break
            else:
                print(f"-> {loc}", end="", file=log)
        if loc < min_location:
            min_location = loc
    print(min_location)
    return min_location


def main_b(data):
    data = parse(data)
    seeds = data.pop("s")
    data["s"] = []
    for i in range(0, len(seeds), 2):
        data["s"] += range(seeds[i], seeds[i] + seeds[i + 1])
    data["s"] = chain(iter(data["s"]))
    return main(data)


testdata = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def test():
    assert main(testdata) == 35
    assert main_b(testdata) == 46


if __name__ == "__main__":
    from sys import argv, stdin

    PART = argv[1] if len(argv) > 1 else "b"
    if not stdin.isatty():
        data = stdin.read()
    else:
        # because year and day can be found in path of this file
        # aocd can determine which data to pull automatically.
        from aocd import data

    main(data) if PART == "a" else main_b(data)
