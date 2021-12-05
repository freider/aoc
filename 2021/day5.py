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
        #print(nums)
        # p1 = Point(nums[0:2])
        # p2 = Point(nums[2:])
        #
        p1 = tuple(nums[0:2])
        p2 = tuple(nums[2:])
        if p1[0] == p2[0]:
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                hits[(p1[0], y)] = hits.get((p1[0], y), 0) + 1
        elif p1[1] == p2[1]:
            for y in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                hits[(y, p1[1])] = hits.get((y, p1[1]), 0) + 1

    print(sum(1 for v in hits.values() if v > 1))


def part2():
    src = aoc_input()
#     src = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2"""
    lines = tolines(src)
    hits = {}
    for line in lines:
        nums = ints(line)
        #print(nums)
        # p1 = Point(nums[0:2])
        # p2 = Point(nums[2:])
        #
        p1 = tuple(nums[0:2])
        p2 = tuple(nums[2:])
        if p1[0] == p2[0]:
            for y in range(min(p1[1], p2[1]), max(p1[1], p2[1]) + 1):
                hits[(p1[0], y)] = hits.get((p1[0], y), 0) + 1
        elif p1[1] == p2[1]:
            for y in range(min(p1[0], p2[0]), max(p1[0], p2[0]) + 1):
                hits[(y, p1[1])] = hits.get((y, p1[1]), 0) + 1
        else:
            diffx = p2[0] - p1[0]
            diffy = p2[1] - p1[1]
            num = abs(diffx)
            diff = np.array([diffx//num, diffy//num])
            c = np.array([p1[0], p1[1]])
            #print(p1, p2)

            for _ in range(num + 1):
                #print(tuple(c))
                hits[tuple(c)] = hits.get(tuple(c), 0) + 1
                c += diff

    print(sum(1 for v in hits.values() if v > 1))


if __name__ == "__main__":
    part1()
    part2()
