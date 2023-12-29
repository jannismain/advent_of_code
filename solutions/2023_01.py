#!/usr/bin/env python
import re


def main(data):
    # extract first and last digit from text using re
    n = 0
    for line in data.splitlines():
        digits = re.findall(r"\d", line)
        v = int(digits[0] + digits[-1])
        n += v
    print(n)
    return n

t = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8", "nine": "9"}
tp = rf"{'|'.join(t.keys())}"

def main_b(data):
    n = 0
    for line in data.splitlines():
        if matches := list(
            map(lambda x: x.group(1), re.finditer(fr'(?=({tp}|\d))', line))
        ):
            v = (matches[0], matches[-1])
            v = int("".join([t.get(x, x) for x in v]))
            n += v
            print(f"{line} -> {matches} -> {v}")
        else:
            print(f"{line} -> no matches")
    print(n)
    return n


def test():
    assert main("""1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet""") == 142
    assert main_b("""two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen""") == 281


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
