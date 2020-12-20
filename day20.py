from collections import defaultdict, namedtuple, Counter

import sys
import re
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp
from lib.input import aoc_input, np_map, pb_input

transform = namedtuple("transform", "rot flipx flipy")
transforms = []
for r in range(2):
    for fx in range(2):
        for fy in range(2):
            transforms.append(transform(r, fx, fy))

def dotrans(t, trans):
    tt = np.copy(t)
    if trans.rot:
        tt = tt.T
    if trans.flipx:
        tt = tt[::-1,::]
    if trans.flipy:
        tt = tt[::,::-1]
    return tt

def part1():
    lines = aoc_input().strip()
    raw = lines.split("\n\n")
    tiles = {}
    for r in raw:
        lines = r.split("\n")
        id = int(lines[0].split(" ")[1].strip(":"))
        tile = np.array([[1 if c == "#" else 0 for c in l] for l in lines[1:]], dtype=int)
        tiles[id] = tile
    alt = defaultdict(set)
    for tid, t in tiles.items():
        for trans in transforms:
            tt = dotrans(t, trans)
            alt[tuple(tt[0,::])].add((tid, trans))

    uniq = defaultdict(int)
    for e, comb in alt.items():
        tids = set(x[0] for x in comb)
        if len(tids) == 1:
            uniq[next(iter(tids))] += 1

    print(uniq.values())
    m = 1
    for u, l in uniq.items():
        if l == 4:
            print(u)
            m *= u
    print(m)
    #print(tiles)


def part2():
    lines = aoc_input().strip().split('\n')



if __name__ == "__main__":
    part1()
    part2()
