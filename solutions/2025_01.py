#!/usr/bin/env python

from dataclasses import dataclass
from typing import Any, Literal


@dataclass
class DialRotation:
    direction: Literal["R", "L"]
    degrees: int

    def __str__(self):
        return f"{self.direction}{self.degrees}"


def parse(data: str) -> list[DialRotation]:
    result = []
    for line in data.splitlines():
        if line[0] not in ("R", "L"):
            raise ValueError(f"Unknown direction: {line[0]}")
        result.append(DialRotation(direction=line[0], degrees=int(line[1:])))
    return result


DIAL_STEPS = 100
INITIAL_DIAL_STATE = 50


def main(data):
    if isinstance(data, str):
        data = parse(data)

    dial_state = INITIAL_DIAL_STATE
    password = 0
    for entry in data:
        if entry.direction == "R":
            dial_state = (dial_state + entry.degrees) % DIAL_STEPS
        elif entry.direction == "L":
            dial_state = (dial_state - entry.degrees) % DIAL_STEPS
        print(f"The dial is rotated {entry} to point at {dial_state}.")
        if dial_state == 0:
            password += 1

    answer = password

    print(answer)
    return answer


def main_b(data):
    if isinstance(data, str):
        data = parse(data)

    dial_state = INITIAL_DIAL_STATE
    password = 0
    for entry in data:
        full_revolutions = entry.degrees // DIAL_STEPS
        remaining_ticks = entry.degrees % DIAL_STEPS

        times_dial_pointed_at_zero = full_revolutions

        if entry.direction == "R":
            new_dial_state = (dial_state + remaining_ticks) % DIAL_STEPS
            if new_dial_state < dial_state:
                times_dial_pointed_at_zero += 1
        elif entry.direction == "L":
            new_dial_state = (dial_state - remaining_ticks) % DIAL_STEPS
            if new_dial_state > dial_state and dial_state != 0:
                times_dial_pointed_at_zero += 1
            if new_dial_state == 0:
                times_dial_pointed_at_zero += 1
        else:
            raise ValueError(f"Unknown direction: {entry.direction}")
        dial_state = new_dial_state
        password += times_dial_pointed_at_zero
        print(
            f"The dial is rotated {entry} to point at {dial_state}{'.' if times_dial_pointed_at_zero == 0 else f'; during this rotation, it pointed to zero {times_dial_pointed_at_zero}x'}"
        )

    answer = password

    print(answer)
    return answer


testdata = """
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82
""".strip()


def test():
    assert main(testdata) == 3
    try:
        assert main("C100")
        assert False
    except ValueError:
        assert True
    assert main_b(testdata) == 6
    assert main_b("R1000") == 10
    assert main_b("L50\nR100") == 2


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
