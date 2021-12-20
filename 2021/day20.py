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
    src = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..##
#..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###
.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#.
.#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#.....
.#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#..
...####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.....
..##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###"""
    src = aoc_input()
    ch = chunks(src)
    bi = ch[0].replace('\n', '')
    m = np_map(ch[1])
    ps = set()
    for (y, x), c in np.ndenumerate(m):
        if c == '#':
            ps.add((y, x))

    infcol = False

    offsetgrid = np.mgrid[-1:2,-1:2].reshape(2, -1).T

    for i in range(50):
        print(i)
        minx = 1e10
        miny = 1e10
        maxx = -1e10
        maxy = -1e10
        for y, x in ps:
            minx = min(minx, x)
            maxx = max(maxx, x)
            miny = min(miny, y)
            maxy = max(maxy, y)
        mins = np.array([miny, minx])
        maxs = np.array([maxy, maxx])

        nextpoints = set()
        box_points = np.mgrid[miny-1:maxy+2, minx-1:maxx+2].reshape(2, -1).T
        for p in box_points:
            neigh = offsetgrid + p
            l = 0
            for n in neigh:
                l *= 2
                l += int(tuple(n) in ps or (infcol and ((n < mins).any() or (n > maxs).any())))

            if bi[l] == '#':
                nextpoints.add(tuple(p))

        if bi[0] == '#' and bi[-1] == '.':
            infcol = not infcol

        ps = nextpoints

    print(len(ps))

    # WA: 5772

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
