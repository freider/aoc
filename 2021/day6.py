import sys
import re
from collections import Counter, defaultdict

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines as tolines, ints
from lib.point import Point


def part1():
    src = aoc_input()
    #src = """3,4,3,1,2"""
    nums = ints(src)
    for i in range(80):
        eights = sum(1 for r in nums if r == 0)
        p = [(n - 1) if n != 0 else 6 for n in nums]
        p += ([8] * eights)
        nums = p
    print(len(nums))

def part2():
    src = aoc_input()
    #src = """3,4,3,1,2"""
    nums = ints(src)
    cnt = Counter(nums)
    print(cnt.items())

    for i in range(256):
        nxt = defaultdict(int)
        for v, n in cnt.items():
            if v == 0:
                nxt[6] += n
                nxt[8] += n
            else:
                nxt[v - 1] += n
        cnt = nxt

    print(sum(cnt.values()))



if __name__ == "__main__":
    part1()
    part2()
