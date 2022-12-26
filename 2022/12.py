#!/usr/bin/env python

from dataclasses import dataclass
import colorama

vectors = [(1, 0), (0, 1), (-1, 0), (0, -1)]

DOWN = 0
RIGHT = 1
UP = 2
LEFT = 3


@dataclass
class Metadata:
    dead_ends: list[tuple[int]]
    dead_end: bool = False
    visited: bool = False

def next_char(c):
    return chr(ord(c) + 1)


def previous_char(c):
    return chr(ord(c) - 1)


def x_to_a(c):
    while ord(c := previous_char(c)) >= ord("a"):
        yield c


TARGET = next_char("z")


def main(data):
    # replace start and end markers, so characters unicode-position strictly increases
    # throughout the algorithm

    data = data.replace("S", previous_char("a"))
    data = data.replace("E", next_char("z"))

    # split by line so indexing by row and column works
    data = data.splitlines()

    # find start position
    for row_idx, row in enumerate(data):
        if (col_idx := row.find(previous_char("a"))) != -1:
            i, j = row_idx, col_idx
            break
    else:
        raise RuntimeError("Couldn't find start position")

    # create array of metadata with same shape as input data
    metadata = [[Metadata([]) for _ in range(len(data[0]))] for _ in range(len(data))]

    path: list[tuple[str,tuple[int]]] = []
    step = 0

    while True:
        # mark current field as visited
        metadata[i][j].visited = True
        step += 1

        # display maze for debugging purposes
        if step % 10 == 0 and ord(data[i][j]) >= ord("c"):
            show(data, metadata, i, j)

        # optimize path
        for p in path:


        # are we done?
        if data[i][j] == TARGET:
            break

        # can we step in any direction?
        step_taken = False
        for step_goal in [next_char(data[i][j]), data[i][j], *x_to_a(data[i][j])]:
            # first, we are looking to step on the next character in any direction
            # if we didn't take a step, we are looking to step on the same character
            # if we found a dead end, we go back one step and mark this direction as dead
            if step_taken:
                break
            for direction in [DOWN, RIGHT, UP, LEFT]:
                r, c = vectors[direction]

                # do not step into dead ends again
                if (r, c) in metadata[i][j].dead_ends:
                    continue

                # do not backtrack by accident (backtracking must be done at the very end)
                if path and (-r, -c) == path[-1][1]:
                    continue

                # do not step past edges
                try:
                    next_letter = data[i + r][j + c]
                except IndexError:
                    continue

                # do not visit the same field twice
                if metadata[i + r][j + c].visited:
                    continue

                if next_letter == step_goal:
                    i += r
                    j += c
                    print(
                        f"'{data[i-r][j-c]}' ({i-r:2d},{j-c:2d}) --({r:-2d},{c:-2d})--> '{data[i][j]}' ({i:2d},{j:2d})"
                    )
                    # save this step in path
                    path.append((data[i][j], (r, c)))
                    step_taken = True
                    break
            else:
                if step_goal == "a":
                    print(f"We found a dead end at ({i}, {j}). Backtracking one step.")
                    metadata[i][j].dead_end = True
                    r, c = path.pop()[1]
                    i -= r
                    j -= c
                    metadata[i][j].dead_ends.append((r, c))
                    step_taken = True
                    break

    print(path)
    print(len(path))
    return len(path)


def show(data, metadata: list[list[Metadata]], i, j):
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if (r, c) == (i, j):
                color = colorama.Back.BLACK
            elif metadata[r][c].dead_end:
                color = colorama.Back.RED
            elif metadata[r][c].visited:
                color = colorama.Back.GREEN
            elif data[r][c] == "a":
                color = colorama.Fore.BLUE
            elif data[r][c] == "b":
                color = colorama.Fore.YELLOW
            elif data[r][c] == "c":
                color = colorama.Fore.MAGENTA
            elif data[r][c] == "n":
                color = colorama.Fore.BLUE
            elif data[r][c] == "o":
                color = colorama.Fore.YELLOW
            elif data[r][c] == "p":
                color = colorama.Fore.MAGENTA
            else:
                color = colorama.Style.DIM
            print(color, end="")
            print(char, end="")
            print(colorama.Style.RESET_ALL, end="")
        print("")


def main_b(data):
    main(data)


def test():
    assert main(testdata) == 31


testdata = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


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
