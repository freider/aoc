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
    src = """939
7,13,x,x,59,x,31,19"""
    src = aoc_input()
    l1, l2 = lines(src)
    n = int(l1)
    bs = ints(l2)

    minw = 1e10
    minb = None
    for b in bs:
        w = b - n % b
        if minb is None or w < minw:
            minb = b
            minw = w

    print(minw * minb)


def part2():
    src = """939
7,13,x,x,59,x,31,19"""
    #src = aoc_input()
    l1, l2 = lines(src)
    n = int(l1)
    bs = tokens(l2)
    def f(a, b):
        i, x = a
        j, y = b

        return (j, x + y)

    print(reduce(f, ((a, b) for (a, b) in enumerate(bs) if b != 'x')))
    # t = 7x
    # 13y = 59z - 3


#211111-908

if __name__ == "__main__":
    part1()
    part2()
