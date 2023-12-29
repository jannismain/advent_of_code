#!/usr/bin/env python

from dataclasses import dataclass


@dataclass
class Monkey:
    items: list[int]
    operation: str
    test_divisible_by: int
    throw_to: list[int]
    items_handled: int = 0


def main(data, part="a"):
    data += "\n\n"
    monkeys: list[Monkey] = []
    for idx, line in enumerate(data.splitlines()):
        if idx % 7 == 1:
            starting_items = [int(d.strip()) for d in line.split(":")[1].split(",")]
        if idx % 7 == 2:
            operation = line.split("=")[1]
        if idx % 7 == 3:
            test_divisible_by = int(line.split()[-1])
        if idx % 7 == 4:
            when_true_throw_to = int(line.split()[-1])
        if idx % 7 == 5:
            when_false_throw_to = int(line.split()[-1])
        if idx % 7 == 6:
            monkeys.append(
                Monkey(
                    starting_items,
                    operation,
                    test_divisible_by,
                    [when_false_throw_to, when_true_throw_to],
                )
            )

    magic_number = lcm(*[monkey.test_divisible_by for monkey in monkeys])

    for _ in range(20 if part == "a" else 10000):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop(0)
                monkey.items_handled += 1
                item = eval(monkey.operation, dict(old=item))
                item = item // 3 if part == "a" else item % magic_number
                throw_to = monkey.throw_to[item % monkey.test_divisible_by == 0]
                monkeys[throw_to].items.append(item)

    checksum = sorted(m.items_handled for m in monkeys)
    print(checksum[-1] * checksum[-2])
    return monkeys


def main_b(data):
    main(data, part="b")


def prime_factors(n):
    todo = [n]
    pf = []
    while todo:
        x = todo.pop()
        for i in range(2, x + 1):
            if (x % i) == 0:
                pf.append(i)
                if (f := x // i) > 1:
                    todo.append(f)
                break
    return pf


def divisors(n):
    return {x for x in range(2, n + 1) if n % x == 0}


def gcd(a, b) -> int:
    try:
        return sorted(divisors(a) & divisors(b))[-1]
    except IndexError:
        return 1


def lcm(*args) -> int:
    args = list(args)
    while args:
        a = args.pop()
        b = args.pop()
        lcm = int(abs(a * b) / gcd(a, b))
        if not args:
            return lcm
        else:
            args.append(lcm)
    return


def test():
    monkeys = main(testdata, "a")
    assert len(monkeys) == 4
    assert [m.items_handled for m in monkeys] == [101, 95, 7, 105]

    monkeys = main(testdata, "b")
    assert len(monkeys) == 4
    assert [m.items_handled for m in monkeys] == [52166, 47830, 1938, 52013]


testdata = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()


if __name__ == "__main__":
    from sys import argv, stdin

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        # because year and day can be found in path of this file
        # aocd can determine which data to pull automatically.
        from aocd import data
    # test()
    main(data) if PART == "a" else main_b(data)
