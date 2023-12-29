#!/usr/bin/env python

def main(data):
    dirs = {"/": 0}
    stack = []
    for line in data.splitlines():
        if line.startswith("$"):
            cmd, *argv = line[1:].strip().split(" ")
            match cmd:
                case "cd":
                    if argv[0] == "..":
                        prevdir = stack.pop()
                    else:
                        stack.append(argv[0])
        elif line.startswith("dir"):
            dname = line.split()[-1]
            if dname not in dirs:
                dirs[dname] = 0
        else:
            fsize, fname = line.split()
            # add file size to current directory
            for cd in stack:
                dirs[cd]+=int(fsize)
    dsizes_relevant = [size for size in dirs.values() if size <= 100000]
    checksum = sum(dsizes_relevant)
    print(dirs)
    print(checksum)
    return checksum, dirs

def test():
    data = """$ cd /\n$ ls\ndir a\n14848514 b.txt\n8504156 c.dat\ndir d\n$ cd a\n$ ls\ndir e\n29116 f\n2557 g\n62596 h.lst\n$ cd e\n$ ls\n584 i\n$ cd ..\n$ cd ..\n$ cd d\n$ ls\n4060174 j\n8033020 d.log\n5626152 d.ext\n7214296 k"""
    checksum, dirs = main(data)
    assert checksum == 95437
    assert dirs == {
        "e":584,
        "a":94853,
        "d":24933642,
        "/":48381165,
    }



def main_b(data):
    main(data)


if __name__ == "__main__":
    from sys import argv, stdin

    YEAR, DAY = 2022, 7

    PART = argv[1] if len(argv) > 1 else "a"
    if not stdin.isatty():
        data = stdin.read()
    else:
        from aocd import get_data

        data = get_data(day=DAY, year=YEAR)

    main(data) if PART == "a" else main_b(data)
