#!/usr/bin/env python


def parse(data: str):
    print(data)


def main(data):
    if isinstance(data, str):
        data = parse(data)


def main_b(data):
    return main(data)


testdata = """
"""


def test():
    assert main(testdata) == 0
    assert main_b(testdata) == 0


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
