#!/usr/bin/env python


def parse(data: str):
    return [[c for c in line] for line in data.splitlines()]


def get_n_surrounding(data, r, c):
    n = 0
    if r + 1 < len(data) and c + 1 < len(data[0]):
        n += int(data[r + 1][c + 1] in "@x")
    if r + 1 < len(data) and c - 1 >= 0:
        n += int(data[r + 1][c - 1] in "@x")
    if r + 1 < len(data):
        n += int(data[r + 1][c] in "@x")
    if c + 1 < len(data[0]):
        n += int(data[r][c + 1] in "@x")
    if c - 1 >= 0:
        n += int(data[r][c - 1] in "@x")
    if r - 1 >= 0 and c + 1 < len(data[0]):
        n += int(data[r - 1][c + 1] in "@x")
    if r - 1 >= 0 and c - 1 >= 0:
        n += int(data[r - 1][c - 1] in "@x")
    if r - 1 >= 0:
        n += int(data[r - 1][c] in "@x")
    return n


def main(data) -> tuple[int, list[list[str]]]:
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for r, _ in enumerate(data):
        for c, value in enumerate(data[r]):
            if value == "@":
                if get_n_surrounding(data, r, c) < 4:
                    answer += 1
                    data[r][c] = "x"

    print(answer)
    return answer, data


def main_b(data):
    data = parse(data)
    answer = 0
    while True:
        n, data = main(data)
        [print("".join(data[r])) for r, _ in enumerate(data)]

        for r, _ in enumerate(data):
            for c, v in enumerate(data[r]):
                if v == "x":
                    data[r][c] = "."

        [print("".join(data[r])) for r, _ in enumerate(data)]

        answer += n
        if n == 0:
            break

    print(answer)
    return answer


testdata = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
""".strip()


def test():
    n, _ = main(testdata)
    assert n == 13
    assert main_b(testdata) == 43


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
