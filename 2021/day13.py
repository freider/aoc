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
    src = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""
    src = aoc_input()
    cs = chunks(src)
    points = []
    for l in lines(cs[0]):
        points.append(ints(l))

    maxx, maxy = np.max(np.array(points), axis=0)

    m = np.zeros((maxy + 1, maxx + 1), dtype=int)
    for p in points:
        m[p[1], p[0]] = 1

    for i, instr in enumerate(lines(cs[1])):
        val, = ints(instr)
        if 'y' in instr:
            m = m[:val, :] + m[(val + 1):, :][::-1, :]
        else:
            m = m[:, :val] + m[:, (val + 1):][:, ::-1]

        if i == 0:
            print((m >= 1).sum())

    for row in m:
        rendered = ''.join('#' if c > 0 else ' ' for c in row)
        print(rendered)

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
