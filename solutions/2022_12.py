#!/usr/bin/env python

from dataclasses import dataclass
import colorama

DOWN = (1, 0)
RIGHT = (0, 1)
UP = (-1, 0)
LEFT = (0, -1)

global directions
directions = (DOWN, RIGHT, UP, LEFT)


@dataclass
class Metadata:
    dead_ends: list[tuple[int]]
    dead_end: bool = False
    visited: bool = False
    shortest_path: bool = False


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
    i, j = start_i, start_j = find_start_position(data, previous_char("a"))

    return find_any_path_and_optimize_it(data, (start_i, start_j))
    # TODO: implement BFS search


def find_start_position(data, marker):
    for row_idx, row in enumerate(data):
        if (col_idx := row.find(previous_char("a"))) != -1:
            return row_idx, col_idx
    raise RuntimeError("Couldn't find start position")


def find_any_path_and_optimize_it(data, initial: tuple[int]):
    N_ROWS = len(data)
    N_COLS = len(data[0])

    # create array of metadata with same shape as input data
    metadata = [[Metadata([]) for _ in range(len(data[0]))] for _ in range(len(data))]

    path: list[tuple[str, tuple[int]]] = []
    i, j = initial[0], initial[1]

    while True:
        # mark current field as visited
        metadata[i][j].visited = True

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
            for direction in directions:
                r, c = direction

                # do not step into dead ends again
                if (r, c) in metadata[i][j].dead_ends:
                    continue

                # do not backtrack by accident (backtracking must be done at the very end)
                if path and (-r, -c) == path[-1][1]:
                    continue

                # do not wrap around the maze (i.e. leave at one side and come out the other)
                if not (0 <= i + r < N_ROWS and 0 <= j + c < N_COLS):
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
                    # print(
                    #     f"'{data[i-r][j-c]}' ({i-r:2d},{j-c:2d}) --({r:-2d},{c:-2d})--> '{data[i][j]}' ({i:2d},{j:2d})"
                    # )
                    # save this step in path
                    path.append(((i, j), (r, c)))
                    step_taken = True
                    break
            else:
                if step_goal == "a":
                    # print(f"We found a dead end at ({i}, {j}). Backtracking one step.")
                    metadata[i][j].dead_end = True
                    r, c = path.pop()[1]
                    i -= r
                    j -= c
                    metadata[i][j].dead_ends.append((r, c))
                    step_taken = True
                    break

    # we found a path, now we need to optimize it so it becomes the shortest path
    # show(data, metadata, i, j)

    shortest_path = []

    i, j, next_pos = initial[0], initial[1], None
    for p_idx, p in enumerate(path):
        p_pos, p_vec = p

        if next_pos is not None and p_pos != next_pos:
            # skip this position, as a closer one has already been found
            continue
        else:
            # caught up with closest position to target, resume normal
            next_pos = None

        # add position to optimal path
        shortest_path.append((p_pos, p_vec))
        # move to this position
        i, j = i + p_vec[0], j + p_vec[1]

        # look for neighbouring field closer to target than actual next field
        p_extra_idx = len(path)
        for p2_pos, p2_vec in path[-1 : p_idx + 1 : -1]:
            p_extra_idx -= 1
            # check if field is neighbour that can be reached
            if get_distance(p_pos, p2_pos) == 1 and can_reach(
                data[p_pos[0]][p_pos[1]], data[p2_pos[0]][p2_pos[1]]
            ):
                shortest_path.append((p2_pos, get_vector(p_pos, p2_pos)))
                # remember next position, so everything "in between" can be removed
                next_pos = p2_pos

    for p, _ in shortest_path:
        metadata[p[0]][p[1]].shortest_path = True

    show(data, metadata, initial[0], initial[1])

    print(len(shortest_path))
    return len(shortest_path)


def get_distance(p1: tuple[int], p2: tuple[int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_vector(p1: tuple[int], p2: tuple[int]):
    return p2[0] - p1[0], p2[1] - p1[1]


def can_reach(c1, c2):
    return ord(c2) <= ord(c1) + 1


def show(data, metadata: list[list[Metadata]], i, j):
    for r, row in enumerate(data):
        for c, char in enumerate(row):
            if (r, c) == (i, j):
                color = colorama.Back.BLACK
            elif metadata[r][c].shortest_path:
                color = colorama.Back.BLUE
            elif metadata[r][c].dead_end:
                color = colorama.Fore.LIGHTRED_EX
            elif metadata[r][c].visited:
                color = colorama.Back.GREEN
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

    from itertools import permutations

    min_steps = 9999
    for direction in permutations((DOWN, UP, LEFT, RIGHT)):
        directions = direction
        print(f"Movement Rules: {directions}")
        min_steps = min(main(data) if PART == "a" else main_b(data), min_steps)
    print(min_steps)
