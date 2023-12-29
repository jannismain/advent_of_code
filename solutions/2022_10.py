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

    return checksum, register

def main_b(data):
    register = main(data)[1]
    line = ""
    sprite = list(40*".")
    sprite[:3] = 3*"#"
    for idx, (sprite_pos_before, sprite_pos_after) in enumerate(register):
        if idx%40 == 0 and idx!=0:
            line+="\n"
        if sprite_pos_after != sprite_pos_before:
            sprite = list(40*".")
            sprite[sprite_pos_after-1:sprite_pos_after+2] = 3*"#"
        line = f"{line}{sprite[idx%40]}"
        # print(f"After cycle {idx+1:02d}\nCurrent CRT row: {line}", file=stderr)
        # print(f"Sprite position: {''.join(sprite)}", file=stderr)
        # print("\n")
    print("REHPRLUB")
    return line

def test():
    assert main(testdata)[0] == [420,1140,1800,2940,2880,3960]

def test_b():
    assert main_b(testdata)

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
