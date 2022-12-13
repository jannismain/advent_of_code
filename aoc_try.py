#!/usr/bin/env python

from os import environ
import pathlib
import json
import subprocess
from datetime import datetime, timedelta
from sys import stderr, stdout
from typing import Optional

import typer

app = typer.Typer()

boilerplate = pathlib.Path(__file__).with_name("boilerplate.py")


@app.command()
def main(
    cmd: Optional[str] = typer.Argument(""),
    year: int = 2022,
    day: int = datetime.now().day,
    part="a",
    test: bool = False,
    show_stats: bool = False,
):
    from aocd import get_data, submit, AocdError

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

    data = get_data(year=year, day=day)
    fp_script = pathlib.Path(f"{year}/{day:02d}.py")

    fp_stats = pathlib.Path(typer.get_app_dir("aoc-try", force_posix=True)) / "stats.json"
    fp_stats.parent.mkdir(exist_ok=True, parents=True)
    stats = json.load(fp_stats.open()) if fp_stats.is_file() else {}
    if f"{year}" not in stats:
        stats[f"{year}"] = {}
    stats_this_year = stats[f"{year}"]
    if show_stats:
        echo_stats(stats)
        exit(0)

    if not fp_script.is_file():
        if typer.confirm(f"Create new solution script for {year}/{day:02d}?", default=True):
            fp_script.parent.mkdir(exist_ok=True)
            fp_script.open("w").write(
                boilerplate.open().read().replace("YEAR, DAY = 2021, 1", f"YEAR, DAY = {year}, {day}")
            )
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
    print(f"Answer: {answer.splitlines()[-1]}")
    if typer.confirm("Submit?"):
        try:
            submit(answer, part=part, year=year, day=day)

            # update stats on first successful submission
            if task in stats_this_year and "ended" not in stats_this_year[task]:
                stats_this_year[task]["ended"] = now()
                stats_this_year[task]["duration"] = int(
                    (
                        datetime.fromisoformat(stats[f"{year}"][task]["ended"])
                        - datetime.fromisoformat(stats[f"{year}"][task]["started"])
                    ).total_seconds()
                )
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
            if "duration" in results:
                typer.secho(f"- {task} solved in {timedelta(seconds=results['duration'])}")
            else:
                typer.secho(f"- {task} unsolved")


if __name__ == "__main__":
    app()
