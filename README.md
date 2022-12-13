# Advent of Code Helpers

`try`:

* create boilerplate solution script
* automatically retrieve puzzle input (via `aocd`)
* submit solutions
* collect stats on when each quiz was started and finished

## Installation

```sh
pip install git+https://github.com/jannismain/advent_of_code.git
```

## Configuration

Follow [`aocd`'s Quickstart guide](https://github.com/wimglenn/advent-of-code-data) to provide your AOC cookie/token either as `AOC_SESSION` environment variable or as `~/.config/aocd/token` file.

## Usage

```console
// Start working on today's puzzle
$ try
Create new solution script for 2022/06? [Y/n]: y

// [...solving today's puzzle...]

// Submit answer to today's puzzle
$ try
XXXXX
Answer: XXXXX
Submit? [y/N]: y

// [...solving part b of today's puzzle...]

// Submitting part b for today's puzzle
$ try b
XXXXX
YYYYY
Answer: YYYYY
Submit? [y/N]: y

// Start working on puzzle of day 1
$ try 1
Create new solution script for 2022/01? [Y/n]: y

// Submitting part b for puzzle of day 1
$ try 1b
ZZZZZ
Answer: ZZZZZ
Submit? [y/N]: y

// Start working on puzzle for day 8 of 2020
$ try 202008
Create new solution script for 2020/08? [Y/n]: y

// Show stats
$ try -

// Run tests for today's puzzle
$ try t

// Run tests for puzzle of day 12
$ try 12t
...
======= 1 passed in 0.00s =======
```

### Start new puzzles

If a given puzzle has no corresponding solution script yet, `try` will offer to generate a boilerplate script for you:

```console
$ try
Create new solution script for 2022/06? [Y/n]:
```

### Submitting puzzle solutions

If `try` finds a solution script for the given puzzle, it will execute the script with the input data (retrieved by `aocd`) and read the solution from stdout. Script output given on `stderr` is echoed and ignored. If multiple lines are found on `stdout`, only the last one is considered as the answer.

```console
$ try
XXXXX
12345
Answer: 12345
Submit? [y/N]: y
```

### Testing puzzle solutions

If a `test()` method was implemented in the solution script, it can be executed by pointing pytest to the script or simply appending `t` to the task argument given to `try`.

```console
$ try 12t
...
======= 1 passed in 0.00s =======
```

### Statistics

`try` will save timestamps of when you started with a quiz (i.e. the time, it generated the solution script for you) and when you submitted the correct solution.

To see the time between start of quiz and submission of correct solution:

```console
$ try -
2021
- 1a solved in  0:02:10
2022
- 9a solved in 20:23:27
- 9b solved in  2:21:07
- 10a solved in 0:06:22
- 10b solved in 0:59:08
```
