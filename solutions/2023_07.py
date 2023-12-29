#!/usr/bin/env python


_FIVE_OF_A_KIND = 7
_FOUR_OF_A_KIND = 6
_FULL_HOUSE = 5
_THREE_OF_A_KIND = 4
_TWO_PAIRS = 3
_ONE_PAIR = 2
_HIGH_CARD = 1


class Hand:
    SCORE = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "J": 11,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
    }

    def __init__(self, cards):
        self.cards = cards

    def count(self, c):
        return str.count(self.cards, c)

    @property
    def primary_score(self):
        for k in self.SCORE:
            if self.count(k) == 5:
                return _FIVE_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) == 4:
                return _FOUR_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) == 3:
                for k2 in self.SCORE:
                    if self.count(k2) == 2:
                        return _FULL_HOUSE
        for k in self.SCORE:
            if self.count(k) == 3:
                return _THREE_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) == 2:
                for k2 in self.SCORE:
                    if self.count(k2) == 2 and k != k2:
                        return _TWO_PAIRS
        for k in self.SCORE:
            if self.count(k) == 2:
                return _ONE_PAIR

        return _HIGH_CARD

    @property
    def secondary_score(self):
        return tuple(self.SCORE[c] for c in self.cards)

    def __str__(self):
        return self.cards

    def __repr__(self):
        return self.cards

    def __lt__(self, other):
        if self.primary_score == other.primary_score:
            return self.secondary_score < other.secondary_score
        return self.primary_score < other.primary_score

    def __le__(self, other):
        if self.primary_score == other.primary_score:
            return self.secondary_score <= other.secondary_score
        return self.primary_score <= other.primary_score

    def __eq__(self, other):
        return (
            self.primary_score == other.primary_score and self.secondary_score == other.secondary_score
        )

    def __ne__(self, other):
        return self.primary_score != other.primary_score or self.secondary_score != other.secondary_score

    def __ge__(self, other):
        if self.primary_score == other.primary_score:
            return self.secondary_score >= other.secondary_score
        return self.primary_score >= other.primary_score

    def __gt__(self, other):
        if self.primary_score == other.primary_score:
            return self.secondary_score > other.secondary_score
        return self.primary_score > other.primary_score


class HandB(Hand):
    SCORE = {
        "A": 14,
        "K": 13,
        "Q": 12,
        "T": 10,
        "9": 9,
        "8": 8,
        "7": 7,
        "6": 6,
        "5": 5,
        "4": 4,
        "3": 3,
        "2": 2,
        "J": 1,
    }

    @property
    def primary_score(self):
        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 5:
                return _FIVE_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 4:
                return _FOUR_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 3:
                for k2 in self.SCORE:
                    if k2 not in {"J", k} and self.count(k2) == 2:
                        return _FULL_HOUSE
        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 3:
                return _THREE_OF_A_KIND

        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 2:
                for k2 in self.SCORE:
                    if self.count(k2) == 2 and k != k2:
                        return _TWO_PAIRS
        for k in self.SCORE:
            if self.count(k) + (self.count("J") if k != "J" else 0) == 2:
                return _ONE_PAIR

        return _HIGH_CARD


def parse(data: str):
    for line in data.splitlines():
        yield (Hand(line[:5]), int(line[5:].strip()))


HAND, BID = 0, 1


def main(data):
    if isinstance(data, str):
        games = sorted(parse(data))
    else:
        games = data
    result = 0
    for rank in range(1, len(games) + 1):
        print(result, "+=", games[rank - 1], "*", rank)
        result += games[rank - 1][BID] * rank
    print(result)
    return result


def main_b(data):
    games = sorted([(HandB(line[:5]), int(line[5:].strip())) for line in data.splitlines()])
    return main(games)


testdata = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""


def test():
    assert sorted([Hand("3AAAA"), Hand("KKKKK"), Hand("A2345"), Hand("AAAA3")]) == [
        Hand("A2345"),
        Hand("3AAAA"),
        Hand("AAAA3"),
        Hand("KKKKK"),
    ]
    assert main(testdata) == 6440
    assert main_b(testdata) == 5905


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
