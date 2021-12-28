import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """0,3,6"""
    src = aoc_input()
    nums = ints(src)
    last_x = dict((x, i) for i, x in enumerate(nums[:-1]))
    lastnum = nums[-1]

    for i in range(len(nums), 30000000):
        last_i = last_x.get(lastnum, i - 1)
        spoken = i - 1 - last_i
        last_x[lastnum] = i - 1
        lastnum = spoken

    print(lastnum)


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
