#!/usr/bin/env python


from math import inf
from types import SimpleNamespace


def parse(data: str):
    fresh_ranges, ingredients = data.split("\n\n")
    fresh_ranges = sorted([list(int(x) for x in rng.split("-")) for rng in fresh_ranges.splitlines()])
    ingredients = [int(x) for x in ingredients.splitlines()]
    return SimpleNamespace(fresh_ranges=fresh_ranges, ingredients=ingredients)


def is_fresh(ingredient, fresh_ranges):
    for rng in fresh_ranges:
        if ingredient in range(rng[0], rng[1] + 1):
            return True
    return False


def main(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for ingredient in data.ingredients:
        answer += int(is_fresh(ingredient, data.fresh_ranges))

    print(answer)
    return answer


def main_b(data):
    data = parse(data)
    answer = 0

    non_overlapping_ranges = [data.fresh_ranges[0]]
    for rng in data.fresh_ranges[1:]:
        s, e = rng
        ls, le = non_overlapping_ranges[-1]
        if s <= le:
            non_overlapping_ranges[-1] = (ls, max(le, e))
        else:
            non_overlapping_ranges.append(rng)

    for rng in non_overlapping_ranges:
        answer += rng[1] - rng[0] + 1

    print(answer)
    return answer


testdata = """
3-5
10-14
16-20
12-18

1
5
8
11
17
32
""".strip()


def test():
    assert main(testdata) == 3
    assert main_b(testdata) == 14


if __name__ == "__main__":
    from sys import argv, stdin

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        # because year and day can be found in path of this file
        # aocd can determine which data to pull automatically.
        from aocd import data

    main(data) if PART == "a" else main_b(data)
