#!/usr/bin/env python

from math import prod

CUBES_AVAILABLE = {"red": 12, "green": 13, "blue": 14}

def main(data, part="a"):
    result = 0
    for game_record in data.splitlines():
        game_id, game_data = game_record.split(":", maxsplit=1)
        game_id = int(game_id.replace("Game ", ""))
        print(game_record, " -> ", f"#{game_id} ", end="")
        cubes_found = dict.fromkeys(CUBES_AVAILABLE, float("-inf"))
        for game_set in game_data.split(";"):
            set_ok = False
            for game_result in game_set.strip().split(","):
                n, c = game_result.strip().split(" ")
                n = int(n)
                cubes_found[c] = max(cubes_found[c], n)
                if n > CUBES_AVAILABLE[c] and part == "a":
                    break
            else:
                set_ok = True
            if not set_ok:
                if part == "a":
                    print("❌")
                    break
        else:
            if part=="a":
                print("✅")
            else:
                print(cubes_found)

            if part == "a":
                result += game_id
        if part=="b":
            result += prod(cubes_found.values())
    print(result)
    return result

def CubesExceeded(Exception):
    pass

def main_b(data):
    return main(data, part="b")


def test():
    assert main("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""") == 8
    assert main("""Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""", part="b") == 2286


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
