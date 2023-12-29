#!/usr/bin/env python


import logging


def main(data, part="a"):
    grid = [["."]]
    snake = []
    snake_length = 10 if part == "b" else 2
    for _ in range(snake_length):
        snake.append([0,0])

    for line in data.splitlines():
        head = snake[0]
        logging.debug(f"\n{line.strip()}\n")
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
            # if necessary, adjust vertical grid size
            if missing_rows:=max(head[0]+r*s - (len(grid) - 1), 0):
                for _ in range(missing_rows):
                    grid.append(list(len(grid[0])*"."))
            if missing_rows:=min(head[0]+r*s, 0):
                for _ in range(abs(missing_rows)):
                    grid.insert(0, list(len(grid[0])*"."))
                    for el in snake:
                        el[0] += 1
        if c:
            # if necessary, adjust horizontal grid size
            if missing_cols:=max(head[1]+c*s - (len(grid[0]) - 1), 0):
                [row.extend(list(missing_cols*".")) for row in grid]
            if missing_cols:=min(head[1]+c*s, 0):
                for _ in range(abs(missing_cols)):
                    [row.insert(0, ".") for row in grid]
                    for el in snake:
                        el[1] += 1

        for n_steps, step_vector in ((c, (0,s)), (r, (s,0))):
            for _ in range(n_steps):
                _move_head(grid, snake, step_vector)
                _move_tail(grid, snake)

        show(grid)

    # how many positiions did the tail visit?
    tail = snake[-1]
    grid[tail[0]][tail[1]] = "#"
    t_visited = 0
    for row in grid:
        t_visited+=row.count("#")
    print(t_visited)
    return t_visited

def _move_head(grid, snake, vector):
    head = snake[0]
    # move head
    if grid[head[0]][head[1]] == "H": # reset position only head visited
        grid[head[0]][head[1]] = "."
    for idx, _ in enumerate(head):
        head[idx] += vector[idx]
    if grid[head[0]][head[1]] == ".": # only overwrite irrelevant markers
        grid[head[0]][head[1]] = "H"

def _move_tail(grid, snake):
    for idx in range(1, len(snake)):
        head = snake[idx-1]
        tail = snake[idx]

        if head == tail:
            continue

        if idx == len(snake) - 1:  # mark past positions of last segment only
            grid[tail[0]][tail[1]] = f"#"
        elif grid[tail[0]][tail[1]] != "#":  # reset other markers
            grid[tail[0]][tail[1]] = f"."

        if abs(tail[0]-head[0]) > 1:
            tail[0] += -1 if tail[0]-head[0] > 0 else 1
            # tail[1] = head[1]
            if abs(tail[1]-head[1]) >= 1:
                tail[1] += -1 if tail[1]-head[1] > 0 else 1
        if abs(tail[1]-head[1]) > 1:
            tail[1] += -1 if tail[1]-head[1] > 0 else 1
            if abs(tail[0]-head[0]) >= 1:
                tail[0] += -1 if tail[0]-head[0] > 0 else 1
            # tail[0] = head[0]
        if grid[tail[0]][tail[1]] != "#":  # do not overwrite relevant markers
            grid[tail[0]][tail[1]] = f"{idx}"

def show(grid):
    [logging.debug("".join(row)) for row in grid]

testdata = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".strip()

testdata_b = """
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".strip()

def test():
    import os
    part = os.getenv("PART", "a")
    assert main(testdata if part=="a" else testdata_b, part) == 13 if part=="a" else 36


def main_b(data, part="b"):
    main(data, part)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 9

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data, PART) if PART == "a" else main_b(data)
