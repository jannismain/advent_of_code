#!/usr/bin/env python


def parse(data: str):
    return data.splitlines()


def main(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for batteries in data:
        v = set()
        for i in range(len(batteries)):
            for j in range(len(batteries)):
                if j <= i:
                    continue
                v.add(int(f"{batteries[i]}{batteries[j]}"))
        max_joltage = max(v)
        answer += max_joltage

    print(answer)
    return answer


def main_b(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    n_batteries_to_activate = 12
    length_of_battery_sequence = len(data[0])

    for batteries in data:
        v = []
        start_at = 0
        for i in range(n_batteries_to_activate):
            remaining_batteries_to_activate = n_batteries_to_activate - i
            first_possible = start_at
            last_possible = length_of_battery_sequence - remaining_batteries_to_activate + 1
            rng = batteries[first_possible:last_possible]
            next = max([int(x) for x in rng])
            start_at += batteries[start_at:].find(str(next)) + 1
            v.append(str(next))
        max_joltage = int("".join(v))
        answer += max_joltage

    print(answer)
    return answer


testdata = """
987654321111111
811111111111119
234234234234278
818181911112111
""".strip()


def test():
    assert main(testdata) == 357
    assert main_b(testdata) == 3121910778619


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
