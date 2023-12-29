#!/usr/bin/env python


def main(data):
    prev = 99999
    n = 0
    for d in data.splitlines():
        d = int(d)
        if d > prev:
            n += 1
        prev = d
    print(n)


def test():
    ...


def main_b(data):
    main(data)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2021, 1

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data) if PART == "a" else main_b(data)
