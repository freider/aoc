import sys
import re
from collections import Counter, defaultdict, deque

import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    src = aoc_input()
    edges = defaultdict(list)
    for line in lines(src):
        a, b = line.split('-')
        edges[a].append(b)
        edges[b].append(a)

    paths = set()
    q = deque([('start', ('start',), {'start'})])
    while q:
        n, path, vis = q.popleft()
        if n == 'end':
            paths.add(path)
            continue
        for next in edges[n]:
            if next.islower() and next in vis:
                continue
            q.append((next, path + (next,), vis | {next}))
    # for p in paths:
    #     print(p)
    print(len(paths))

def part2():
    src = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
    src = aoc_input()
    edges = defaultdict(list)
    for line in lines(src):
        a, b = line.split('-')
        edges[a].append(b)
        edges[b].append(a)

    paths = set()
    q = deque([('start', ('start',), {'start'}, None)])
    while q:
        n, path, vis, vist = q.popleft()
        if n == 'end':
            paths.add(path)
            continue
        for next in edges[n]:
            if next == 'start':
                continue
            if next.islower():
                if next not in vis:
                    q.append((next, path + (next,), vis | {next}, vist))
                elif vist is None:
                    q.append((next, path + (next,), vis, next))
                else:
                    continue
            else:
                q.append((next, path + (next,), vis, vist))

    print(len(paths))


if __name__ == "__main__":
    part1()
    part2()
