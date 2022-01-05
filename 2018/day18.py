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
from scipy.ndimage import correlate

def part1():
    src = """.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|."""
    src = aoc_input()
    m = np_map(src)
    neigh = [[1, 1, 1], [1, 0, 1], [1, 1, 1]]
    def nextm(m):
        empty = correlate((m == '.') * 1, neigh, mode='constant')
        yards = correlate((m == '#') * 1, neigh, mode='constant')
        trees = correlate((m == '|') * 1, neigh, mode='constant')
        newm = m.copy()
        for yx, c in np.ndenumerate(m):
            if c == "." and trees[yx] >= 3:
                newm[yx] = '|'
            elif c == "|" and yards[yx] >= 3:
                newm[yx] = "#"
            elif c == "#" and not (yards[yx] >= 1 and trees[yx] >= 1):
                newm[yx] = '.'
        return newm

    def tupm(m):
        return tuple(tuple(row) for row in m)
    
    seen = {}

    for it in range(10):
        seen[tupm(m)] = it
        m = nextm(m)

    print(((m == '#') * 1).sum() * ((m == '|') * 1).sum())

    from itertools import count

    for it in count(10):
        t = tupm(m)
        if t in seen:
            if (1000000000 - it) % (it - seen[t]) == 0:
                print(((m == '#') * 1).sum() * ((m == '|') * 1).sum())
                break
        else:
            seen[t] = it

        nxt = nextm(m)
        if (nxt == m).all():
            break
        m = nxt


# toolow: 184004

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
