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
    src = """F10
N3
F7
R90
F11"""
    src = aoc_input()
    p = Point(0, 0)
    dir = Point(0, 1)

    for l in lines(src):
        c, n = l[0], int(l[1:])
        if c == 'N':
            p += Point(n, 0)
        if c == 'S':
            p += Point(-n, 0)
        if c == 'W':
            p += Point(0, -n)
        if c == 'E':
            p += Point(0, n)
        if c == 'L':
            dir = dir.rot90(k=3 * (n // 90))
        if c == 'R':
            dir = dir.rot90(k=1 * (n // 90))
        if c == 'F':
            p += dir * n
    print(abs(p[0]) + abs(p[1]))


def part2():
    src = """F10
N3
F7
R90
F11"""
    src = aoc_input()
    p = Point(0, 0)
    wp = Point(1, 10)

    for l in lines(src):
        c, n = l[0], int(l[1:])
        if c == 'N':
            wp += Point(n, 0)
        if c == 'S':
            wp += Point(-n, 0)
        if c == 'W':
            wp += Point(0, -n)
        if c == 'E':
            wp += Point(0, n)
        if c == 'L':
            wp = wp.rot90(k=3 * (n // 90))
        if c == 'R':
            wp = wp.rot90(k=1 * (n // 90))
        if c == 'F':
            p += wp * n
    print(abs(p[0]) + abs(p[1]))


if __name__ == "__main__":
    part1()
    part2()
