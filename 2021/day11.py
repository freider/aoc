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
        m += 1

        def flash(p):
            m[p] = 10
            for _next in neighbours8(m, p):
                next = tuple(_next)
                if m[next] != 10:
                    m[next] += 1
                    if m[tuple(next)] == 10:
                        flash(tuple(next))

        mcpy = m.copy()
        for (y, x), c in np.ndenumerate(mcpy):
            if c == 10:
                flash((y, x))

        numflash = ((m == 10)*1).sum()
        total += numflash
        m[m == 10] = 0

    print(total)


def part2():
    src = aoc_input()
    m = np.vectorize(int)(np_map(src))
    total = 0
    for step in range(1, 1000000):
        m += 1

        def flash(p):
            m[p] = 10
            for _next in neighbours8(m, p):
                next = tuple(_next)
                if m[next] != 10:
                    m[next] += 1
                    if m[tuple(next)] == 10:
                        flash(tuple(next))

        mcpy = m.copy()
        for (y, x), c in np.ndenumerate(mcpy):
            if c == 10:
                flash((y, x))

        numflash = ((m == 10)*1).sum()
        total += numflash
        m[m == 10] = 0
        if (m == 0).all():
            break

    print(step)


if __name__ == "__main__":
    part1()
    part2()
