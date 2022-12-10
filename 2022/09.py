#!/usr/bin/env python


def main(data):
    grid = [["."]]
    pos_h = [0,0]

    def show(grid):
        [print("".join(row)) for row in grid]

    pos_t = [pos_h[0],pos_h[1]]
    grid[pos_h[0]][pos_h[1]] = "H"
    for idx, line in enumerate(data.splitlines()):
        direction, n = line.split(" ")
        s = 1
        n = int(n)
        match direction:
            case "U":
                r, c = n,0
                # switching direction of up and down, as going up means decreasing index
                s = -1
            case "D":
                r, c = n,0
            case "L":
                r, c = 0,n
                s = -1
            case "R":
                r, c = 0,n
        if r:
            # adjust vertical grid size
            if missing_rows:=max(pos_h[0]+r*s - (len(grid) - 1), 0):
                for _ in range(missing_rows):
                    grid.append(list(len(grid[0])*"."))
            if missing_rows:=min(pos_h[0]+r*s, 0):
                for _ in range(abs(missing_rows)):
                    grid.insert(0, list(len(grid[0])*"."))
                    pos_h[0] += 1
                    pos_t[0] += 1

            for _ in range(r):
                # move head
                if grid[pos_h[0]][pos_h[1]] == "H": # reset position only head visited
                    grid[pos_h[0]][pos_h[1]] = "."
                pos_h[0] += s
                if grid[pos_h[0]][pos_h[1]] == ".": # don't overwrite more important tail positions
                    grid[pos_h[0]][pos_h[1]] = "H"

                # move tail
                grid[pos_t[0]][pos_t[1]] = "#"
                # move horizontally/vertically, if horizontal/vertical distance between head and tail is greater than 1
                if abs(pos_t[0]-pos_h[0]) > 1:
                    pos_t[0] += -1 if pos_t[0]-pos_h[0] > 0 else 1
                    pos_t[1] = pos_h[1]
                if abs(pos_t[1]-pos_h[1]) > 1:
                    pos_t[1] += 1 if pos_t[1]-pos_h[1] > 0 else -1
                    pos_t[0] = pos_h[0]
                grid[pos_t[0]][pos_t[1]] = "T"
        if c:
            # adjust horizontal grid size
            if missing_cols:=max(pos_h[1]+c*s - (len(grid[0]) - 1), 0):
                [row.extend(list(missing_cols*".")) for row in grid]
            if missing_cols:=min(pos_h[1]+c*s, 0):
                for _ in range(abs(missing_cols)):
                    [row.insert(0, ".") for row in grid]
                    pos_h[1] += 1
                    pos_t[1] += 1

            for _ in range(c):
                # move head
                if grid[pos_h[0]][pos_h[1]] == "H": # reset position only head visited
                    grid[pos_h[0]][pos_h[1]] = "."
                pos_h[1] += s
                if grid[pos_h[0]][pos_h[1]] == ".": # don't overwrite more important tail positions
                    grid[pos_h[0]][pos_h[1]] = "H"

                # move tail
                grid[pos_t[0]][pos_t[1]] = "#"
                if abs(pos_t[0]-pos_h[0]) > 1:
                    pos_t[0] += 1 if pos_t[0]-pos_h[0] > 0 else -1
                    pos_t[1] = pos_h[1]
                if abs(pos_t[1]-pos_h[1]) > 1:
                    pos_t[1] += -1 if pos_t[1]-pos_h[1] > 0 else 1
                    pos_t[0] = pos_h[0]
                grid[pos_t[0]][pos_t[1]] = "T"

    # how many positiions did the tail visit?
    grid[pos_t[0]][pos_t[1]] = "#"
    t_visited = 0
    for row in grid:
        t_visited+=row.count("#")
    print(t_visited)
    return t_visited

testdata = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".strip()

def test():
    assert main(testdata) == 13


def main_b(data):
    main(data)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 9

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)
    # test()
    main(data) if PART == "a" else main_b(data)
