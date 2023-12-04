#!/usr/bin/env python

from math import prod

symbols = set("*#+$&@%/-=")


def main(data):
    result = []
    n = 0
    grid = [list(line) for line in data.splitlines()]
    # add padding around grid's edge to simplify index checking
    grid.insert(0, ["."] * len(grid[0]))
    grid.append(["."] * len(grid[0]))
    for row in grid:
        row.insert(0, ".")
        row.append(".")
    print("\n".join("".join(row) for row in grid))
    for ri, row in enumerate(grid):
        number, number_counts, detecting_number = "", False, False
        for ci, s in enumerate(row):
            if s.isdigit():
                detecting_number = True
                number += s
                # check for adjacent symbol
                if not number_counts and (
                    grid[ri][ci + 1] in symbols
                    or grid[ri][ci - 1] in symbols
                    or grid[ri + 1][ci] in symbols
                    or grid[ri - 1][ci] in symbols
                    or grid[ri + 1][ci + 1] in symbols
                    or grid[ri - 1][ci - 1] in symbols
                    or grid[ri + 1][ci - 1] in symbols
                    or grid[ri - 1][ci + 1] in symbols
                ):
                    number_counts = True
            elif detecting_number:  # end of number
                detecting_number = False
                if number_counts:
                    result.append(int(number))
                number = ""
                number_counts = False
        if detecting_number:  # end of row
            detecting_number = False
            if number_counts:
                result.append(int(number))
            number_counts = False
    print(result)
    print(sum(result))
    return sum(result)


def main_b(data):
    gears = {
        (r, c): []
        for r, row in enumerate(data.splitlines())
        for c, s in enumerate(row)
        if s == "*"
    }
    print(gears)

    for ri, row in enumerate(data.splitlines()):
        number, adjacent_gear, detecting_number = "", False, False
        for ci, s in enumerate(row):
            if s.isdigit():
                detecting_number = True
                number += s
                # check for adjacent gear
                if not adjacent_gear:
                    for coord in [
                        (ri + 1, ci),
                        (ri - 1, ci),
                        (ri, ci + 1),
                        (ri, ci - 1),
                        (ri + 1, ci + 1),
                        (ri - 1, ci - 1),
                        (ri + 1, ci - 1),
                        (ri - 1, ci + 1),
                    ]:
                        if coord in gears:
                            adjacent_gear = coord
                            break
            elif detecting_number:  # end of number
                detecting_number = False
                if adjacent_gear:
                    gears[adjacent_gear].append(int(number))
                number = ""
                adjacent_gear = None
        if detecting_number:  # end of row
            detecting_number = False
            if adjacent_gear:
                gears[adjacent_gear].append(int(number))
            number = ""
            adjacent_gear = None
    gear_ratios = sum(prod(gears[coord]) for coord in gears if len(gears[coord]) == 2)
    print(gear_ratios)
    return gear_ratios


data = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def test():
    assert main(data) == 4361
    assert main_b(data) == 467835


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
