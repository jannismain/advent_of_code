#!/usr/bin/env python


def parse(data):
    results = []
    for row in data.splitlines():
        winning_numbers, numbers = row.split(": ")[1].split(" | ")
        winning_numbers = {int(x) for x in winning_numbers.split(" ") if x.isnumeric()}
        numbers = [int(x) for x in numbers.split(" ") if x.isnumeric()]
        results.append([winning_numbers, numbers, 1])
    return results


def main(data, multiplier=1):
    cards = parse(data)
    total_score = 0
    for card in cards:
        winning_numbers, numbers, n = card
        score = 0
        for number in numbers:
            if number in winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        total_score += score
    print(total_score)
    return total_score


N = 2


def main_b(data):
    cards = parse(data)
    for idx, card in enumerate(cards):
        score = 0
        winning_numbers, numbers, n = card
        for number in numbers:
            if number in winning_numbers:
                score += 1
        for copy_idx in range(1, score + 1):
            cards[idx + copy_idx][N] += cards[idx][N]
    n_cards = sum(card[N] for card in cards)
    print(n_cards)
    return n_cards


test_data = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def test():
    assert main(test_data) == 13
    assert main_b(test_data) == 30


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
