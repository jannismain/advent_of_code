#!/usr/bin/env python

MAPPING = {
    "A": "ROCK",
    "B": "PAPER",
    "C": "SCISSORS",
    "X": "ROCK",
    "Y": "PAPER",
    "Z": "SCISSORS",
}
SCORE_WIN = 6
SCORE_DRAW = 3

WIN_TABLE = {
    "ROCK": "PAPER",
    "PAPER": "SCISSORS",
    "SCISSORS": "ROCK",
}

SCORES = {
    "ROCK": 1,
    "PAPER": 2,
    "SCISSORS": 3,
}


def main(data):
    score = 0
    for line in data.splitlines():
        n, m = [MAPPING[c] for c in line.split()]
        # score according to the choice I made
        score += SCORES[m]
        # score according to the outcome of the game
        if m == n:  # draw
            score += SCORE_DRAW
        elif m == WIN_TABLE[n]:
            score += SCORE_WIN
    print(score)


def main_b(data):
    score = 0
    for line in data.splitlines():
        n_, m_ = line.split()
        n = MAPPING[n_]
        match m_:
            case "X": # loose to opponent
                score += SCORES[WIN_TABLE[WIN_TABLE[n]]]
            case "Y": # match opponent for draw
                score += SCORES[n] + SCORE_DRAW
            case "Z": # win against opponent
                score += SCORES[WIN_TABLE[n]] + SCORE_WIN
    print(score)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 2

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data) if PART == "a" else main_b(data)
