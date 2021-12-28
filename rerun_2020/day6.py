import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints, lines
from lib.point import Point


def part1():
    src = aoc_input()
    #src = """"""
    a = 0
    for c in chunks(src):
        a += len(Counter(''.join(c.split())).keys())
    print(a)


def part2():
    src = aoc_input()
    #src = """"""
    a = 0
    for c in chunks(src):
        allsets = []
        for l in lines(c):
            allsets.append(set(l))
        a += len(set.intersection(*allsets))

    print(a)


if __name__ == "__main__":
    part1()
    part2()
