import sys
import re
from collections import Counter, defaultdict
from itertools import count

from scipy.ndimage import correlate

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point



dirs = np.array([np.array([y, x]) for x in (-1, 0, 1) for y in (-1, 0, 1) if not (x == y == 0)])

# def part1():
#     src = aoc_input()
#     m = np_map(src)
#     h, w = m.shape
#
#     for i in range(10000000):
#         nextm = m.copy()
#         for (y, x), c in np.ndenumerate(m):
#             box = m[max(0, y - 1):min(h, y+2), max(0, x - 1):min(w, x + 2)]
#             if c == 'L' and ((box == '#') * 1).sum() == 0:
#                 nextm[y, x] = '#'
#             elif c == '#' and ((box == '#') * 1).sum() >= 5:
#                 nextm[y, x] = 'L'
#         if (nextm == m).all():
#             break
#         m = nextm
#
#     print(((m == '#') * 1).sum())
def one_iter_p2(m):
    out = np.empty_like(m, dtype=str)
    for (y, x), v in np.ndenumerate(m):
        loc = np.array([y, x])
        ocount = 0
        for d in dirs:
            for n in count(1):
                p = loc + d * n
                if ((p >= 0) & (p < m.shape)).all():
                    if m[p[0], p[1]] == "#":
                        ocount += 1
                        break
                    if m[p[0], p[1]] == "L":
                        break
                else:
                    break

        if v == "#" and ocount >= 5:
            out[y, x] = "L"
        elif v == "L" and ocount == 0:
            out[y, x] = "#"
        else:
            out[y, x] = v
    return out


def part2():
    m = np_map(aoc_input().strip())
    while 1:
        out = one_iter_p2(m)
        if (m == out).all():
            break
        m = out
    return np.sum(m == "#")

def part1_opt():
    src = """L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL"""
    src = aoc_input()
    m = np_map(src)

    for i in range(10000000):
        nocc = correlate(
            (m == "#") * 1,
            [[1, 1, 1],
             [1, 0, 1],
             [1, 1, 1]],
            mode='constant',
        )
        newm = m.copy()
        newm[(m == "#") & (nocc >= 4)] = 'L'
        newm[(m == "L") & (nocc == 0)] = '#'
        if np.all(newm == m):
            break
        m = newm
    print(m)
    print((m == "#").sum())




if __name__ == "__main__":
    import time
    t0 = time.perf_counter()
    part2()
    t1 = time.perf_counter()
    print(t1 - t0)
    #part1_opt()
    #print(time.perf_counter() - t1)
    #part2()
