#!/usr/bin/env python


def parse(data: str):
    print(data)
    rv = [tuple(map(int, r.split("-"))) for r in data.split(",")]
    return rv


def main(data):
    if isinstance(data, str):
        data = parse(data)

    answer = 0

    for rng in data:
        print(f"{rng[0]}-{rng[1]}")
        for id in range(rng[0], rng[1] + 1):
            sid = str(id)
            lsid = len(sid)

            # checking for numbers repeated twice
            if sid[0 : lsid // 2] * 2 == sid:
                print(sid)
                answer += int(sid)

    print(answer)
    return answer


def main_b(data):
    answer = 0
    data = parse(data)
    for rng in data:
        print(f"{rng[0]}-{rng[1]}")
        for id in range(rng[0], rng[1] + 1):
            sid = str(id)
            lsid = len(sid)

            # checking for all repeated numbers, not only repeated twice
            found = set()
            for i in range(1, lsid // 2 + 1):
                pref = sid[0:i]
                if lsid % len(pref) == 0:
                    if pref * (lsid // len(pref)) == sid:
                        if sid not in found:
                            print(sid)
                            answer += int(sid)
                        found.add(sid)
    print(answer)
    return answer


testdata = """
11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124
""".strip()


def test():
    # assert main(testdata) == 1227775554
    assert main_b(testdata) == 4174379265


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
