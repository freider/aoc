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
    src = """target area: x=20..30, y=-10..-5"""
    src = aoc_input()
    nums = ints(src, negative=True)
    xran = nums[:2]
    yran = nums[2:]

    besty = 0
    for vy in range(1000):
        y = 0
        highest = 0
        for s in range(1000):
            y += vy
            highest = max(y, highest)
            vy -= 1
            if yran[0] <= y <= yran[1]:
                besty = max(besty, highest)
                break
            elif y < yran[0]:
                break
    print(besty)

    # steps_from_top = -miny // 2
    #
    #
    #
    # 1 + 2 + 3 + 4 ... = Y
    #
    # def exp(s):
    #     falldist = s * (s + 1) / 2
    #     # == 0.5 * s ** 2 + 0.5 s
    #
    #
    #     (s * (s + 1) - (s - 1) * s)/ 2
    #
    #     s ( (s + 1) - (s - 1) ) / 2
    #     s ( - 1 ) / 2
    #
    #     -s/2
    #
    #     steps 5


def part2():
    src = """target area: x=20..30, y=-10..-5"""
    src = aoc_input()
    nums = ints(src, negative=True)
    xran = nums[:2]
    yran = nums[2:]

    worky = set()
    for initvy in range(-100, 1000):
        y = 0
        highest = 0
        vy = initvy
        for s in range(1000):
            y += vy
            highest = max(y, highest)
            vy -= 1
            if yran[0] <= y <= yran[1]:
                worky.add(initvy)
                break
            elif y < yran[0]:
                break

    workv = set()
    for initvy in worky:
        for initvx in range(xran[1] + 1):
            x = y = 0
            vx = initvx
            vy = initvy
            for s in range(1000):
                y += vy
                x += vx
                vy -= 1
                if vx > 0:
                    vx -= 1
                if vx < 0:
                    vx += 1
                if yran[0] <= y <= yran[1] and xran[0] <= x <= xran[1]:
                    workv.add((initvy, initvx))
                    break
                elif y < yran[0] or x > xran[1]:
                    break

    print(len(workv))


if __name__ == "__main__":
    part1()
    part2()
