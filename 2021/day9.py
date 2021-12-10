import sys
import re
from collections import Counter, defaultdict, deque

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.grid_2d import neighbours4
from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """2199943210
3987894921
9856789892
8767896789
9899965678"""
    src = aoc_input()
    dirs = [np.array(a) for a in [(-1, 0), (1, 0), (0, 1), (0, -1)]]
    m = np.array([[int(c) for c in w] for w in lines(src)])
    risk = 0
    for (y, x), n in np.ndenumerate(m):
        ismin = True
        for d in dirs:
            p = d + (y, x)
            if ((p >= 0) & (p < m.shape)).all():
                if n >= m[p[0], p[1]]:
                    ismin = False
        if ismin:
            risk += 1 + n

    print(risk)


def part2():
    src = aoc_input()
    m = np.array([[int(c) for c in w] for w in lines(src)])

    def rec(p, col):
        m[p] = col
        neighbours = neighbours4(m, p)
        for t in neighbours:
            if m[tuple(t)] < 9:
                rec(tuple(t), col)

    nextcol = 10
    for pos, col in np.ndenumerate(m):
        if col < 9:
            rec(pos, nextcol)
            nextcol += 1

    counts = Counter(m[m != 9])
    print(np.product(sorted(counts.values())[-3:]))


if __name__ == "__main__":
    part1()
    part2()



