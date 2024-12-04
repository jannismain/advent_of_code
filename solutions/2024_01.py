#!/usr/bin/env python


def parse(data: str) -> tuple[list[int]]:
    print(data)
    return [int(d.split()[0]) for d in data.splitlines()], [int(d.split()[1]) for d in data.splitlines()]


def main(data):
    if isinstance(data, str):
        a, b = parse(data)
    a = sorted(a)
    b = sorted(b)
    print(f"a={a}")
    print(f"b={b}")

    total = 0
    for i, d in enumerate(a):
        distance = d - b[i] if d > b[i] else b[i] - d
        print(d, " ", b[i], " -> ", distance)
        total += distance
    print(total)
    return total


def main_b(data):
    a, b = parse(data)
    total = 0
    for d in a:
        occurences = sum(1 for d2 in b if d == d2)
        subtotal = d * occurences
        print(f"{d} appears {occurences}x in {b} -> {subtotal}")
        total += subtotal
    print(total)
    return total


testdata = """3   4
4   3
2   5
1   3
3   9
3   3
"""


def test():
    assert main(testdata) == 11
    assert main_b(testdata) == 31


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
