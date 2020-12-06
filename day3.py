import sys
import re
from functools import reduce
from operator import mul

from lib.input import aoc_input, np_map
import numpy as np


def solve(step=(1, 3)):
    trees = 0
    pos = np.array([0, 0])
    inp = np_map(aoc_input())
    rowlen = inp.shape[1]
    while pos[0] < len(inp):
        if inp[pos[0], pos[1] % rowlen] == "#":
            trees += 1
        pos += step
    return trees


def part1():
    step = np.array([1, 3])
    print(solve(step))


def part2():
    steps = [
        [1, 1],
        [1, 3],
        [1, 5],
        [1, 7],
        [2, 1],
    ]
    print(reduce(mul, (solve(step) for step in steps), 1))


if __name__ == "__main__":
    part1()
    part2()
