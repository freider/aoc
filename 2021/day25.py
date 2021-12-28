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
    src = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    src = aoc_input()
    m = np_map(src)
    h, w = m.shape

    cows = set((y, x, c) for (y, x), c in np.ndenumerate(m) if c in '>v')
    for i in range(1000):
        totmove = 0
        # eastmoving
        tomove = []
        for y, x, c in cows:
            if c != '>' or (y, (x + 1)%w, '>') in cows or (y, (x + 1)%w, 'v') in cows:
                continue
            tomove.append((y,x,c))
        for y, x, c in tomove:
            cows.remove((y, x, c))
            cows.add((y, (x + 1)%w, c))
        totmove += len(tomove)

        # southmoving
        tomove = []
        for y, x, c in cows:
            if c != 'v' or ((y+1)%h, x, '>') in cows or  ((y+1)%h, x, 'v') in cows:
                continue
            tomove.append((y,x,c))
        for y, x, c in tomove:
            cows.remove((y, x, c))
            cows.add( ((y+1)%h, x, c))
        totmove += len(tomove)

        print(f'{totmove}')
        if totmove == 0:
            break

    print(i + 1)
    # WA: 365, 366 - too low


def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
