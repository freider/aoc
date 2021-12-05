import sys
import re
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

    lines = tolines(src)
    hits = {}
    for line in lines:
        nums = ints(line)

        p1 = Point(*nums[0:2])
        p2 = Point(*nums[2:])
        if np.any(np.equal(p1.v, p2.v)):
            for p in Point.line_points(p1, p2):
                hits[p] = hits.get(p, 0) + 1

    print(sum(1 for v in hits.values() if v > 1))


def part2():
    src = aoc_input()

    lines = tolines(src)
    hits = {}
    for line in lines:
        nums = ints(line)

        p1 = Point(*nums[0:2])
        p2 = Point(*nums[2:])
        for p in Point.line_points(p1, p2):
            hits[p] = hits.get(p, 0) + 1

    print(sum(1 for v in hits.values() if v > 1))



if __name__ == "__main__":
    part1()
    part2()
