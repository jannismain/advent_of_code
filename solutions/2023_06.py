#!/usr/bin/env python


def parse(data: str):
    time, distance = data.splitlines()
    time = [int(x.strip()) for x in time.split()[1:]]
    distance = [int(x.strip()) for x in distance.split()[1:]]
    return list(zip(time, distance))


def main(data):
    if isinstance(data, str):
        data = parse(data)
    result = 1
    for t, d in data:
        t_charge = t // 2
        t_race = t - t_charge
        n_wins = 0
        while t_charge * t_race > d:
            n_wins += 1
            t_charge -= 1
            t_race += 1
        n_wins = n_wins * 2 - (1 if t % 2 == 0 else 0)
        print((t, d), n_wins)
        result *= n_wins
    print(result)
    return result


def main_b(data):
    data = parse(data)
    time = int("".join(str(t) for t, _ in data))
    distance = int("".join(str(d) for _, d in data))
    return main([(time, distance)])


testdata = """Time:      7  15   30
Distance:  9  40  200
"""


def test():
    assert main(testdata) == 288
    assert main_b(testdata) == 71503


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
