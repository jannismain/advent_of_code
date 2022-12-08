# Advent of Code Helpers

`try`:

* automatically retrieve puzzle input (via `aocd`)
* create boilerplate solution script
* submit solutions
* collect stats on when each task was started and finished

## Usage



```sh
# Start working on today's puzzle
try
# [...solving today's puzzle...]
# Submitting today's puzzle
try
# [...solving part b of today's puzzle...]
# Submitting part b for today's puzzle
try b
# Start working on puzzle of day 1
try 1
# Submitting part b for puzzle of day 1
try 1b
# Start working on puzzle for day 8 of 2020
try 202008
...
# Only show stats
try -
# Run tests for today's puzzle
try t
# Run tests for day 12ths puzzle
try 12t
```

### Start new puzzles

If a given puzzle has no corresponding solution script yet, `try` will offer to generate a boilerplate script for you:

```console
$ try
Create new solution script for 2022/06? [Y/n]:
```

### Submitting puzzle solutions

If `try` finds a solution script for the given puzzle, it will execute the script with the input data (retrieved by `aocd`) and read the solution from stdout. Script output given on `stderr` is echoed and ignored.

### Testing puzzle solutions

If a `test()` method was implemented in the solution script, it can be executed by pointing pytest to the script or simply appending `t` to the task argument given to `try`.
