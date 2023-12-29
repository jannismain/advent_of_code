#!/usr/bin/env python


def main(data):
    max_calories = -1
    current_elf = 0
    for calories in data.splitlines():
        match calories:
            case "":
                max_calories = max(current_elf, max_calories)
                current_elf = 0
            case _:
                current_elf += int(calories)
    print(max_calories)

def main_b(data):
    calories_per_elf = []
    current_elf = 0
    for calories in data.splitlines():
        match calories:
            case "":
                calories_per_elf.append(current_elf)
                current_elf = 0
            case _:
                current_elf += int(calories)
    print(sum(sorted(calories_per_elf, reverse=True)[:3]))

if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 1

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main_b(data) if PART == "a" else main_b(data)
