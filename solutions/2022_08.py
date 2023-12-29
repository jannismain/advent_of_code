#!/usr/bin/env python

from math import prod
from sys import stderr


def main(data):
    data = data.splitlines()
    rows, cols = len(data), len(data[0])
    print(f"{rows}x{cols}", file=stderr)
    n_visible = 2 * (rows + cols) - 4
    # max_top, max_bottom, max_left, max_right = 0, 0, 0, 0
    for row in range(1, rows - 1):
        for col in range(1, cols - 1):
            tree = data[row][col]
            for idx, line_of_sight in enumerate(
                [
                    [row[col] for row in data[0:row]],  # top
                    [row[col] for row in data[row + 1 :]],  # bottom
                    data[row][0:col],  # left
                    data[row][col + 1 :],  # right
                ]
            ):
                if all(los < tree for los in line_of_sight):
                    print(
                        f"tree {tree} at {row}x{col} is visible from {['top', 'bottom', 'left', 'right'][idx]} (los: {line_of_sight})",
                        file=stderr,
                    )
                    n_visible += 1
                    break
            line_of_sight_top = [row[col] for row in data[0:row]]
    print(n_visible)
    return n_visible


def test():
    testdata = "30373\n25512\n65332\n33549\n35390"
    assert main(testdata) == 21
    assert main_b(testdata) == 8


def main_b(data):
    data = data.splitlines()
    rows, cols = len(data), len(data[0])
    print(f"{rows}x{cols}", file=stderr)
    max_scenic_score = 0
    for row in range(rows):
        for col in range(cols):
            tree = int(data[row][col])
            scenic_score = [0, 0, 0, 0]
            for idx, line_of_sight in enumerate(
                [
                    reversed([row[col] for row in data[0:row]]),  # top
                    [row[col] for row in data[row + 1 :]],  # bottom
                    reversed(data[row][0:col]),  # left
                    data[row][col + 1 :],  # right
                ]
            ):
                for n in line_of_sight:
                    scenic_score[idx] += 1
                    if int(n) >= tree:
                        break

            tree_score = prod(scenic_score)
            print(
                f"tree {tree} at {row}x{col} has scenic score of {tree_score} ({scenic_score})",
                file=stderr,
            )
            max_scenic_score = max(max_scenic_score, tree_score)
    print(max_scenic_score)
    return max_scenic_score


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 8

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)
    main(data) if PART == "a" else main_b(data)
