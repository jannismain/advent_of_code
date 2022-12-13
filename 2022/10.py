#!/usr/bin/env python


from sys import stderr, stdout


def main(data):
    register = [(1,1)]
    for line in data.splitlines():
        cmd, *args = line.split()
        match cmd:
            case "noop":
                register.append((register[-1][-1], register[-1][-1]))
            case "addx":
                register.append((register[-1][-1], register[-1][-1]))  # last value stays for first cycle
                register.append((register[-1][-1], register[-1][-1]+int(args[0])))

    checksum = []
    for idx in range(20,221,40):
        print(f"{idx}: {register[idx][0]} -> {register[idx][0]*idx}", file=stderr)
        checksum.append((idx)*register[idx][0])
    print(sum(checksum))

    # for idx, v in enumerate(register):
    #     print(f"x[{idx}]: {v}", file=stderr)

    return checksum

def test():
    assert main(testdata) == [420,1140,1800,2940,2880,3960]

testdata = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""


def main_b(data):
    main(data)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 10

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data) if PART == "a" else main_b(data)
