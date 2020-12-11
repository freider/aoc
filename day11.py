from itertools import count

import itertools

import sys
import re
import numpy as np
from functools import reduce
from operator import mul

from scipy.ndimage import convolve

from lib.draw import draw, sparse_to_array
from lib.input import aoc_input, np_map, pb_input

dirs = [np.array(x) for x in set(itertools.product([-1, 0, 1], [-1, 0, 1])) - {(0, 0)}]


def one_iter(m):
    out = np.empty_like(m, dtype=str)
    for (y, x), v in np.ndenumerate(m):
        loc = np.array([y, x])
        ocount = 0
        for d in dirs:
            p = loc + d
            if ((p >= 0) & (p < m.shape)).all():
                ocount += m[p[0], p[1]] == "#"

        if v == "#" and ocount >= 4:
            out[y, x] = "L"
        elif v == "L" and ocount == 0:
            out[y, x] = "#"
        else:
            out[y, x] = v
    return out


def part1():
    m = np_map(aoc_input().strip())
    while 1:
        out = one_iter(m)
        if (m == out).all():
            break
        m = out
    return np.sum(m == "#")


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




if __name__ == "__main__":
    print(part1())
    print(part2())
