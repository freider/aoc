import sys
import re
from collections import Counter

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens


def part1():
    m = np_map(aoc_input(), int)
    b = ''.join(str(x) for x in (np.argmax(np.bincount(a)) for a in m.T))
    a = ''.join(str(x) for x in (np.argmin(np.bincount(a)) for a in m.T))
    print(int(b, 2) * int(a, 2))


def part2():
    src = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""
    #src = aoc_input()
    m = np_map(src, int)
    n = m.copy()
    for i in range(m.shape[1]):
        m = m[m[:, i] == np.argmax(np.bincount(m[:, i]))]
        n = n[n[:, i] == np.argmin(np.bincount(n[:, i]))]

    print(m)
    print(n)





if __name__ == "__main__":
    part1()
    part2()
