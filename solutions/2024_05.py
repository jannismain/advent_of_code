#!/usr/bin/env python

IN_ORDER = []

NOT_IN_ORDER = []


def parse(data: str) -> tuple[list[tuple[int, int]], list[list[int]]]:
    print(data)

    page_ordering_rules, list_of_page_updates = data.split("\n\n")

    page_ordering_rules = [
        (int(line.split("|")[0]), int(line.split("|")[1])) for line in page_ordering_rules.splitlines()
    ]
    list_of_page_updates = [
        [int(x) for x in line.split(",")] for line in list_of_page_updates.splitlines()
    ]

    return page_ordering_rules, list_of_page_updates


def main(data):
    if isinstance(data, str):
        data = parse(data)
    page_ordering_rules, list_of_page_updates = data
    print("page_ordering_rules:", page_ordering_rules)
    print("list_of_page_updates:", list_of_page_updates)

    global IN_ORDER, NOT_IN_ORDER
    answer = 0

    for page_updates in list_of_page_updates:
        print(page_updates)
        for rule in page_ordering_rules:
            try:
                assert page_updates.index(rule[0]) < page_updates.index(rule[1])
            except AssertionError:
                print(f"NOT IN ORDER due to {rule}")
                NOT_IN_ORDER += [page_updates]
                break
            except ValueError:
                continue
        else:
            print("IN ORDER")
            IN_ORDER += [page_updates]
            answer += page_updates[len(page_updates) // 2]

    print(answer)
    return answer


def main_b(data):
    main(data)
    if isinstance(data, str):
        data = parse(data)
    page_ordering_rules, list_of_page_updates = data
    print("page_ordering_rules:", page_ordering_rules)
    print("list_of_page_updates:", list_of_page_updates)

    answer = 0
    global NOT_IN_ORDER

    for page_updates in NOT_IN_ORDER:
        print(page_updates)
        while True:
            in_order = False
            fixed_something = False
            for rule in page_ordering_rules:
                try:
                    assert page_updates.index(rule[1]) > page_updates.index(rule[0])
                except AssertionError:
                    print(f"NOT IN ORDER due to {rule}")
                    idx_before, idx_after = page_updates.index(rule[0]), page_updates.index(rule[1])
                    page_updates.insert(idx_after, page_updates.pop(idx_before))
                    print(f"after revision:\n{page_updates}")
                    fixed_something = True
                    break
                except ValueError:
                    continue
                else:
                    in_order = True
            if not fixed_something and in_order:
                print("IN ORDER")
                answer += page_updates[len(page_updates) // 2]
                break
    print(answer)
    return answer


testdata = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
""".strip()


def test():
    # assert main(testdata) == 143
    assert main_b(testdata) == 123


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
