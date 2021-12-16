import heapq
import sys
import re
from collections import Counter, defaultdict, deque

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.grid_2d import neighbours4
from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point
from lib.numdict import numdict


def part1():
    src = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
    src = aoc_input()
    m = np.vectorize(int)(np_map(src))
    q = [(0, (0, 0))]
    goal = (m.shape[1] - 1, m.shape[0] -1)
    best = {}
    while q:
        c, pos = heapq.heappop(q)
        y, x = pos
        if pos == goal:
            print(c)
            break

        for y2, x2 in neighbours4(m, (y, x)):
            c2 = c + m[(y2, x2)]
            if c2 < best.get((y2, x2), 1e10):
                best[(y2, x2)] = c2
                heapq.heappush(q, (c2, (y2, x2)))

    from networkx import DiGraph, shortest_path_length
    from networkx.algorithms.shortest_paths.generic import shortest_path
    g = DiGraph()
    for (y, x), c in np.ndenumerate(m):
        for y2, x2 in neighbours4(m, (y, x)):
            g.add_edge((y, x), (y2, x2), weight=m[(y2, x2)])
    print(shortest_path_length(g, (0, 0), (m.shape[1] - 1, m.shape[0] -1), 'weight'))
    #WA: 648


def part2():
    src = """8"""
    src = aoc_input()
    mo = np.vectorize(int)(np_map(src))
    h, w = mo.shape
    m = np.zeros((mo.shape[0] * 5, mo.shape[1] * 5), dtype=int)

    def mult(x):
        r = x + 1
        if r > 9:
            r = 1
        return r

    for i in range(5):
        for j in range(5):
            part = mo
            for k in range(i + j):
                part = np.vectorize(mult)(part)
            m[i * h: (i+1) * h, j * w: (j + 1) * h] = part

    q = [(0, (0, 0))]
    goal = (m.shape[1] - 1, m.shape[0] -1)
    best = {}
    while q:
        c, pos = heapq.heappop(q)
        y, x = pos
        if pos == goal:
            print(c)
            break

        for y2, x2 in neighbours4(m, (y, x)):
            c2 = c + m[(y2, x2)]
            if c2 < best.get((y2, x2), 1e10):
                best[(y2, x2)] = c2
                heapq.heappush(q, (c2, (y2, x2)))

    #WA: 2466


if __name__ == "__main__":
    part1()
    part2()
