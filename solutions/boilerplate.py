#!/usr/bin/env python


def parse(data: str):
    print(data)
    return data


def main(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    print(answer)
    return answer


def main_b(data):
    answer = main(data)

    print(answer)
    return answer


testdata = """
<INSERT TESTDATA HERE>
""".strip()


def test():
    assert main(testdata) == 0
    # assert main_b(testdata) == 0


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
