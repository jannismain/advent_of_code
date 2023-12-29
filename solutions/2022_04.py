#!/usr/bin/env python

if __name__ == "__main__":
    from sys import argv

    PART = argv[1] if len(argv) > 1 else "a"

    from sys import stdin

    count = 0
    for assignment in stdin:
        first, second = [[int(i) for i in elf.split("-")] for elf in assignment.split(",")]
        if PART == "a":  # only count fully overlapping assignments
            if (
                first[0] <= second[0]
                and first[1] >= second[1]
                or first[0] >= second[0]
                and first[1] <= second[1]
            ):
                count += 1
        elif PART == "b":  # count all overlapping assignments
            # de-morgan of first[1] < second[0] or first[0] > second[1]
            if first[1] >= second[0] and first[0] <= second[1]:
                count += 1
    print(count)
