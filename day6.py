import sys
import re
import numpy as np
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input


def part1():
    groups = aoc_input().strip().split('\n\n')
    print(sum(len(set("".join(g.split()))) for g in groups))


def part2():
    groups = aoc_input().strip().split('\n\n')

    def e(g):
        return set.intersection(*[set(p) for p in g.split('\n')])

    print(sum(len(e(g)) for g in groups))


if __name__ == "__main__":
    part1()
    part2()
