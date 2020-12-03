from functools import reduce
from operator import mul

import numpy as np


def read():
    with open("inputs/3") as f:
        for line in f:
            yield line.strip()


def solve(step):
    trees = 0
    pos = np.array([0, 0])
    inp = list(read())
    while pos[0] < len(inp):
        trees += 1 if inp[pos[0]][pos[1]] == "#" else 0
        pos += step
        pos[1] = pos[1] % len(inp[0])
    return trees


def part1():
    step = np.array([1, 3])
    print(solve(step))


def part2():
    steps = [
        np.array([1, 1]),
        np.array([1, 3]),
        np.array([1, 5]),
        np.array([1, 7]),
        np.array([2, 1]),
    ]
    print(reduce(mul, (solve(step) for step in steps), 1))


if __name__ == "__main__":
    part1()
    part2()
