#!/usr/bin/env python

# priority correspond to array index + 1
PRIORITIES = list("abcdefghijklmnopqrstuvwxyz")
PRIORITIES += [c.upper() for c in PRIORITIES]


def get_priority(item: str):
    assert len(item) == 1
    return PRIORITIES.index(item) + 1


def main(data):
    checksum = 0
    for line in data.splitlines():
        compartment1, compartment2 = set(line[: len(line) // 2]), set(line[len(line) // 2 :])
        common_items = compartment1 & compartment2
        assert len(common_items) == 1
        checksum += get_priority(common_items.pop())
    print(checksum)


def main_b(data):
    checksum = 0
    data = data.splitlines()
    for idx in range(0, len(data), 3):
        elf1 = set(data[idx + 0])
        elf2 = set(data[idx + 1])
        elf3 = set(data[idx + 2])
        badge = elf1 & elf2 & elf3
        assert len(badge) == 1
        checksum += get_priority(badge.pop())
    print(checksum)


if __name__ == "__main__":
    from sys import argv, stdin

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=3, year=2022)

    main(data) if PART == "a" else main_b(data)
