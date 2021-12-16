import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.grid_2d import neighbours8
from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = aoc_input()
    m = np.vectorize(int)(np_map(src))
    total = 0
    for step in range(100):
        def flash(p):
            if m[p] == 10:
                return
            if m[p] == 9:
                m[p] += 1
                for _next in neighbours8(m, p):
                    flash(tuple(_next))
            else:
                m[p] += 1

        for p, c in np.ndenumerate(m):
            flash(p)

        total += (m == 10).sum()
        m[m == 10] = 0

    print(total)


def part2():
    src = aoc_input()
    m = np.vectorize(int)(np_map(src))
    total = 0
    for step in range(1, 1000000):
        def flash(p):
            if m[p] == 10:
                return
            if m[p] == 9:
                m[p] += 1
                for _next in neighbours8(m, p):
                    flash(tuple(_next))
            else:
                m[p] += 1

        for p, c in np.ndenumerate(m):
            flash(p)

        total += (m == 10).sum()
        m[m == 10] = 0
        if (m == 0).all():
            break

    print(step)


if __name__ == "__main__":
    part1()
    part2()
