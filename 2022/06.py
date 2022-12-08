#!/usr/bin/env python


def main(data):
    MARKER_LENGTH = 4 if PART == "a" else 14

    for pos in range(MARKER_LENGTH, len(data)):
        s = set(data[pos - MARKER_LENGTH : pos])
        if len(s) == MARKER_LENGTH:
            print(pos)
            exit(0)

    print("Marker could not be found!")
    exit(1)


def main_b(data):
    main(data)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 7

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data) if PART == "a" else main_b(data)
