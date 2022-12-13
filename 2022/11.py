#!/usr/bin/env python

from dataclasses import dataclass, field


@dataclass
class Monkey:
    items: list[int]
    operation: str
    test_divisible_by: int
    throw_to: list[int]
    items_handled: int = 0


def main(data):
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

    for monkey in monkeys:
        print(monkey)

    for n_round in range(20):
        for monkey in monkeys:
            for _ in range(len(monkey.items)):
                item = monkey.items.pop(0)
                monkey.items_handled += 1
                item = eval(monkey.operation, dict(old=item))
                item = item // 3
                throw_to = monkey.throw_to[item % monkey.test_divisible_by == 0]
                monkeys[throw_to].items.append(item)
        print(f"\nAfter round {n_round+1}:")
        for idx, monkey in enumerate(monkeys):
            print(f"Monkey {idx}: {monkey.items}")

    checksum = sorted(m.items_handled for m in monkeys)
    print(checksum[-1] * checksum[-2])
    return monkeys


def main_b(data):
    main(data)


def test():
    monkeys = main(testdata)
    assert len(monkeys) == 4
    assert [m.items_handled for m in monkeys] == [101, 95, 7, 105]


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
    test()
    main(data) if PART == "a" else main_b(data)
