import re

from lib.input import aoc_input


def data():
    for line in aoc_input().split('\n'):
        parts = re.split(r"[\s:\-]+", line.strip())
        low, high, c, pw = parts
        yield int(low), int(high), c, pw


def part1():
    print(sum(1 if low <= pw.count(c) <= high else 0 for low, high, c, pw in data()))


def part2():
    def valid(low, high, c, pw):
        return (pw[low - 1] + pw[high - 1]).count(c) == 1

    print(sum(1 if valid(*t) else 0 for t in data()))

if __name__ == "__main__":
    part1()
    part2()
