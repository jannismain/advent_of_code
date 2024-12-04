#!/usr/bin/env python


def parse(data: str):
    print(data)
    parsed = []
    for line in data.splitlines():
        parsed.append([int(d) for d in line.split()])
    print(parsed)
    return parsed


def main(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for report in data:
        increasing = None
        is_safe = True
        print(report)
        for idx, d in enumerate(report[1:], start=1):
            is_safe, increasing = check_safe(d, report[idx - 1], increasing)
            print(f"Looking at {d} → {is_safe}")
            if not is_safe:
                break
        if is_safe:
            answer += 1

    print(answer)
    return answer


def check_safe(b, a, increasing=None) -> tuple[bool, bool]:
    if a == b:
        return False, False
    if increasing is not None:
        if increasing:
            return b > a and b - a < 4, True
        else:
            return a > b and a - b < 4, False
    if a > b:
        return a - b <= 3, False
    else:
        return b - a <= 3, True


def main_b(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for report in data:
        is_safe = False
        off = -1
        while not is_safe and off < len(report):
            increasing = None
            if off >= 0:
                report_to_check = report[:]
                report_to_check.pop(off)
            else:
                report_to_check = report

            print(report_to_check)

            for idx, d in enumerate(report_to_check[1:], start=1):
                is_safe, increasing = check_safe(d, report_to_check[idx - 1], increasing)
                print(f"Looking at {d} → {is_safe}")
                if not is_safe:
                    break
            off += 1
        if is_safe:
            answer += 1
            print("-> SAFE")
        else:
            print("-> NOT SAFE")

    print(answer)
    return answer


testdata = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
""".strip()


def test():
    assert main(testdata) == 2
    assert main_b(testdata) == 4


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
