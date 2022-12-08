#!/usr/bin/env python


def main(data):

    initial, commands = data.split("\n\n", maxsplit=2)
    initial = initial.splitlines()[:-1]
    commands = commands.splitlines()

    # parse crates
    ROWS = len(initial)
    COLS = len(initial[-1].split(" "))

    crates = [[] for _ in range(COLS)]
    for col in range(COLS):
        col_idx = col * 4 + 1
        for row_idx in range(ROWS):
            if (c := initial[row_idx][col_idx]).strip():
                crates[col].insert(0, c)

    CRATEMOVER = 9000 if PART == "a" else 9001

    for cmd in commands:
        # parse command
        _, n, _, idx_from, _, idx_to = cmd.split(" ")
        n = int(n)
        idx_from = int(idx_from) - 1
        idx_to = int(idx_to) - 1

        # execute command
        if CRATEMOVER == 9000:  # moving crates one by one
            for _ in range(n):
                crates[idx_to].append(crates[idx_from].pop())
        elif CRATEMOVER == 9001:  # moving multiple crates at a time
            crates[idx_to].extend(crates[idx_from][-n:])
            del crates[idx_from][-n:]
        else:
            raise RuntimeError("Unsupported CRATE MOVER version")

    print("".join(crate[-1] for crate in crates))


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 7

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data)
