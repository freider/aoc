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
            ps.add(Point(y, x))

    infcol = False

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

        nextpoints = set()
        for p in Point.box_points(Point(miny - 1, minx - 1), Point(maxy + 1, maxx + 1)):
            binstring = []
            for n in p.neighbours():
                outside = ((n.np() < np.array([miny, minx])) | (n.np() > np.array([maxy, maxx]))).any()
                binstring.append(str(int(n in ps or (outside and infcol))))

            b = ''.join(binstring)
            l = int(b, 2)
            if bi[l] == '#':
                nextpoints.add(p)

        if bi[0] == '#' and bi[-1] == '.':
            infcol = not infcol

        ps = nextpoints
        # print('it', i)
        # draw(sparse_to_array({p: 1 for p in ps}), {1: '#', 0: '.'})


    print(len(ps))

    # WA: 5772

def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
