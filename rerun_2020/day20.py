import sys
import re
from collections import Counter, defaultdict

import math
import numpy as np
import networkx as nx
from functools import reduce
from operator import mul
from lib.draw import draw, sparse_to_array
import pyparsing as pp

from lib.input import aoc_input, np_map, pb_input, tokens, chunks, lines, ints
from lib.point import Point


def part1():
    src = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###..."""
    src = aoc_input()
    tiles = {}
    for c in chunks(src):
        cl = lines(c)
        num = int(cl[0][5:-1])
        tiles[num] = np_map('\n'.join(cl[1:]))

    def versions(tile):
        t1 = tile
        t2 = tile.T
        yield t1
        yield t2
        for rot in range(3):
            t1 = np.array([t1[::-1, i] for i in range(t1.shape[1])])
            t2 = np.array([t2[::-1, i] for i in range(t2.shape[1])])
            yield t1
            yield t2

    neighbours = defaultdict(set)
    edgecounts = defaultdict(int)

    for t1 in sorted(tiles.keys()):
        for t2 in sorted(tiles.keys()):
            if t2 > t1:
                for v1 in versions(tiles[t1]):
                    edgecounts[tuple(v1[0])] += 1
                    for v2 in versions(tiles[t2]):
                        if (v1[0] == v2[0]).all():
                            neighbours[t1].add(t2)
                            neighbours[t2].add(t1)

    corners = set()
    for t, neigh in neighbours.items():
        if len(neigh) == 2:
            corners.add(t)
    assert len(corners) == 4
    print(math.prod(corners))

    h = w = int(math.sqrt(len(tiles)))
    placed = [[None] * w for _ in range(h)]

    def usable(y, x, v):
        return True

    def rec(y, x, used):
        for t in set(tiles.keys()) - used:
            for v in versions(tiles[t]):
                if usable(y, x, v):
                    placed[y][x] = v
                    if rec(y + 1, x, used | {t}) and rec(y, x + 1, used | {t}):
                        return True
        return False

    rec(0, 0)

    for y in range(h):
        for x in range(w):
            for t in set(tiles.keys()) - used:
                istopbot = y in (0, h - 1)
                isside = x in (0, w - 1)
                if istopbot and isside and len(neighbours[t]) != 2:
                    continue
                elif (istopbot or isside) and len(neighbours[t]) != 3:
                    continue

                topmatch = None
                leftmatch = None
                if y != 0:
                    topmatch = tuple(placed[y - 1][x][h-1])
                if x != 0:
                    leftmatch = tuple(placed[x - 1][y][:,w-1])

                for v in versions(tiles[t]):
                    if topmatch is None and edgecounts[tuple(v[0])] != 1:
                        continue
                    if leftmatch is None and edgecounts[tuple(v[:,0])] != 1:
                        continue


                    placed[y][x] = v
                    used.add(t)
                    break
                else:
                    continue
                break





def part2():
    pass


if __name__ == "__main__":
    part1()
    part2()
