import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints
from lib.point import Point


def part1():
    src = aoc_input()
    #src = """16,1,2,0,4,2,7,1,2,14"""
    n = np.array(ints(src))
    print(np.abs(n - np.median(n)).sum())


def part2():
    src = aoc_input()
    #src = """16,1,2,0,4,2,7,1,2,14"""
    n = np.array(ints(src))

    mj = 10000000000

    for i in range(max(n)):
        a = np.abs(n - i)
        mj = min(mj, (a * (a + 1) // 2).sum())

    print(mj)


if __name__ == "__main__":
    part1()
    part2()
