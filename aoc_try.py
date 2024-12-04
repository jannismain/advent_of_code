#!/usr/bin/env python

import json
import pathlib
import subprocess
from datetime import datetime
from os import environ
from sys import stderr, stdout
from typing import Optional

import typer

app = typer.Typer()

solution_dir = pathlib.Path(__file__).with_name("solutions")
boilerplate = solution_dir / "boilerplate.py"


@app.command()
def main(
    cmd: Optional[str] = typer.Argument(""),
    year: int = datetime.now().year if datetime.now().month >= 12 else datetime.now().year - 1,
    day: int = datetime.now().day,
    part="a",
    test: bool = False,
    show_stats: bool = False,
    submit: bool = False,
):
    """Download Advent of Code tasks, test and upload your solutions.

    CMD can include the following characters `[<year><day>bt-]`:

    - `<year>`: interact with a task of a different year

    - `<day>`: interact with task of a day other than today

    - `b`: act on part b of the given exercise

    - `t`: run tests rather than download a task or upload a solution

    - `-`: show stats
    """
    from aocd import AocdError, get_data, submit

    # parse mini-command language
    if "b" in cmd:
        part = "b"
        cmd = cmd.replace("b", "")
    if "t" in cmd:
        test = True
        cmd = cmd.replace("t", "")
    if "-" in cmd:
        show_stats = True
        cmd = cmd.replace("-", "")
    if len(cmd) >= 4:
        year = int(cmd[:4])
        cmd = cmd[4:]
    if cmd:
        day = int(cmd)

    task = f"{day}{part}"

    fp_stats = pathlib.Path(typer.get_app_dir("aoc-try", force_posix=True)) / "stats.json"
    fp_stats.parent.mkdir(exist_ok=True, parents=True)
    stats = json.load(fp_stats.open()) if fp_stats.is_file() else {}

    if show_stats:
        echo_stats(stats)
        exit(0)

    if f"{year}" not in stats:
        stats[f"{year}"] = {}
    stats_this_year = stats[f"{year}"]

    fp_script = pathlib.Path(solution_dir / f"{year}_{day:02d}.py")
    if not fp_script.is_file():
        if typer.confirm(f"Create new solution script for {year}_{day:02d}?", default=True):
            fp_script.parent.mkdir(exist_ok=True)
            fp_script.open("w").write(boilerplate.open().read())
            typer.launch(f"https://adventofcode.com/{year}/day/{day}")
            stats_this_year[task] = dict(started=now())
            json.dump(stats, fp_stats.open("w"), indent=2)
        exit(1)
    if test:
        env = environ
        env.update(dict(PART=part))
        result = subprocess.run(["pytest", "-s", fp_script], stdout=stdout, stderr=stderr)
        exit(result.returncode)
    try:
        data_file = pathlib.Path(fp_script.stem)
        try:
            data = data_file.read_text()
        except FileNotFoundError:
            data = get_data(year=year, day=day)
            data_file.open("w").write(data)
        result = subprocess.run(
            ["python", fp_script, part],
            text=True,
            input=data,
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print(e.stdout)
        print(e.stderr)
        exit(1)
    if logs := result.stderr.strip().splitlines():
        [typer.secho(f"{log}", dim=True) for log in logs]
    answer = result.stdout.strip()
    typer.secho(answer)

    answer = answer.splitlines()[-1]
    print(f"Answer: {answer}")
    if submit or typer.confirm("Submit?"):
        try:
            submit(answer, part=part, year=year, day=day)

            # update stats on first successful submission
            if task in stats_this_year and "ended" not in stats_this_year[task]:
                stats_this_year[task]["ended"] = now()
                if task.endswith("a"):
                    stats_this_year[task.replace("a", "b")] = dict(started=now())
                json.dump(stats, fp_stats.open("w"), indent=2)
        except AocdError as e:
            typer.secho(e, err=True, fg="red")
            exit(1)


def now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def echo_stats(stats):
    for year in sorted(stats):
        typer.secho(f"{year}", bold=True)
        for task, results in stats[year].items():
            if "ended" in results:
                ended = datetime.fromisoformat(results["ended"])
                started = datetime.fromisoformat(results["started"])
                typer.secho(f"- {task} solved in {ended-started}")
            else:
                typer.secho(f"- {task} unsolved")


if __name__ == "__main__":
    app()
