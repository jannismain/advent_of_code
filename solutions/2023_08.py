#!/usr/bin/env python
import math


def parse(data: str):
    directions, _, *_graph = data.splitlines()
    graph = {}
    for line in _graph:
        node, connected = line.split(" = ")
        graph[node] = tuple(connected[1:-1].split(", "))
    directions = [0 if x == "L" else 1 for x in directions]
    return directions, graph


def main(data):
    d, graph = parse(data)
    current, i = "AAA", 0
    while True:
        current = graph[current][d[i % len(d)]]
        i += 1
        if current == "ZZZ":
            break
    print(i)
    return i


def main_b(data):
    d, graph = parse(data)
    current = [k for k in graph if k.endswith("A")]
    stats = []
    for _ in current:
        stats.append([])
    i = 0
    while True:
        for idx in range(len(current)):
            current[idx] = graph[current[idx]][d[i % len(d)]]
        i += 1
        if any(k.endswith("Z") for k in current):
            print(f"step {i:04d}", list("X" if k.endswith("Z") else "-" for k in current), flush=True)
            for idx, k in enumerate(current):
                if k.endswith("Z"):
                    stats[idx].append(i)
            for idx, stat in enumerate(stats):
                print(f"{idx}: {stat}")
        if all(len(stat) > 0 for stat in stats):
            break
    result = math.lcm(*[stat[0] for stat in stats])
    print(result)
    return result


testdata = """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

testdata2 = """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

testdata3 = """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""


def test():
    assert main(testdata) == 2
    assert main(testdata2) == 6
    assert main_b(testdata2) == 6
    assert main_b(testdata3) == 6


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
