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


def part2():
    src = """.#.
..#
###"""
    src = aoc_input()
    m = np_map(src)
    active = set()
    for (y, x), v in np.ndenumerate(m):
        if v == '#':
            active.add(Point(0, 0, y, x))

    for it in range(6):
        active_neighbours = defaultdict(int)
        for a in active:
            for n in a.neighbours():
                if n != a:
                    active_neighbours[n] += 1

        next_active = set()
        for p, num in active_neighbours.items():
            if (p in active and num == 2) or num == 3:
                next_active.add(p)
        active = next_active

    print(len(active))






def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
